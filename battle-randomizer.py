import random as rand
import string
import time
from numpy.random import randint
import os
import discord
from dotenv import load_dotenv
import pokebase as pb

#### SETTINGS ####
NUM_RULES = 3
NUM_MONS = 3
TIME_LIMIT = 7
RULE_MAX_BP_RANGE = [50, 130]
RULE_MAX_STAT_RANGE = [40, 100]

SETTING_NATDEX_CHANCE = 50
SETTING_TERASTALLIZE_ON_CHANCE = 50

SPECIES_CLAUSE_ON_CHANCE = 90
MOODY_CLAUSE_ON_CHANCE = 60
OHKO_CLAUSE_ON_CHANCE = 85
EVASION_CLAUSE_ON_CHANCE = 80
ITEM_CLAUSE_ON_CHANCE = 50

ruleset = [
    {"Only mons starting with @": 10},
    {"Only moves starting with @": 10},
    {"Only items starting with @": 10},
    {
        "Only mons that have 1 type": 3,
        "Only mons that are part & type": 10
    },
    {"Damaging moves can only be up to # base power": 10},
    {"No STAB moves allowed (Tera type included if terastallized)": 0},
    {"* stat has to be max !": 10},
    {"All mons have access to the move $ (Use hackmons meta for battle)": 20}
]

#LISTS
types = ["Normal", "Fire", "Water", "Grass", "Electric", "Ice", "Fighting", "Poison", 
         "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy"]
tiers = ["LC", "ZU", "NU", "PU", "RU", "UU", "OU", "Ubers"]
stats = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]
numMoves = 904 #We use pokebase api for moves

def getBattleRules():
    global ruleset
    rules = ruleset
    battleRules = ""
    
    #### CLAUSES ####
    battleRules += str(NUM_MONS) + " MONS, " + str(TIME_LIMIT) + " MINUTE TIME LIMIT\n"
    battleRules += "NATIONAL DEX\n"         if randint(100) <= SETTING_NATDEX_CHANCE else "SV POKEDEX\n"
    battleRules += "Only " + rand.choice(tiers) + " pokemon or below\n"
    battleRules += "TERASTALLIZE ON\n\n" if randint(100) <= SETTING_TERASTALLIZE_ON_CHANCE else "TERASTALLIZE OFF\n\n"

    battleRules += "Species Clause ON\n"    if randint(100) <= SPECIES_CLAUSE_ON_CHANCE else "Species Clause OFF\n"   # Species Clause
    battleRules += "Moody Clause ON\n"      if randint(100) <= MOODY_CLAUSE_ON_CHANCE else "Moody Clause OFF\n"    # Moody Clause
    battleRules += "OHKO Clause ON\n"       if randint(100) <= OHKO_CLAUSE_ON_CHANCE else "OHKO Clause OFF\n"    # OHKO Clause
    battleRules += "Evasion Clause ON\n"    if randint(100) <= EVASION_CLAUSE_ON_CHANCE else "Evasion Clause OFF\n"    # Evasion Clause
    if randint(100) <= ITEM_CLAUSE_ON_CHANCE: battleRules += "Item Clause ON (No 2 pokemon may have the same item)\n"    # Item Clause
    battleRules += "\n"

    #### SELECTED RULES ####
    for i in range(NUM_RULES):
        randNum = randint(sum(v for s in rules for v in s.values()))
        selectedRule = 0
        for s in rules:
            for v in s:
                selectedRule = selectedRule + s[v]
                if selectedRule >= randNum:
                    selectedRule = (v, s[v])
                    break
            if isinstance(selectedRule, tuple): break
        rules = [s for s in rules if s.get(selectedRule[0]) != selectedRule[1]]

        selectedRuleString = selectedRule[0].replace("@", rand.choice(string.ascii_letters).upper())
        selectedRuleString = selectedRuleString.replace("&", rand.choice(types))
        selectedRuleString = selectedRuleString.replace("#", str(randint(RULE_MAX_BP_RANGE[0]/5, RULE_MAX_BP_RANGE[1]/5)*5))
        selectedRuleString = selectedRuleString.replace("*", rand.choice(stats))
        selectedRuleString = selectedRuleString.replace("!", str(randint(RULE_MAX_STAT_RANGE[0]/5, RULE_MAX_STAT_RANGE[1]/5)*5))
        if selectedRuleString.find("$"):
            selectedRuleString = selectedRuleString.replace("$", str(pb.move(randint(1, numMoves))).replace("-", " ").title())
        battleRules += "RULE " + str(i + 1) + ": " + selectedRuleString + "\n\n"
    return battleRules

battleInProgress = False

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(f"{client.user} has connected to the server:"f"{guild.name}(id: {guild.id})")

@client.event
async def on_message(message):
    global battleInProgress
    if message.author == client.user:
        return

    if message.content == "!battle":
        if (battleInProgress):
            channel = client.get_channel(int(os.getenv("MAIN_CHANNEL")))
            await channel.send("Battle already in progress!")
        else:
            channel = client.get_channel(int(os.getenv("BATTLE_CHANNEL")))
            battleInProgress = True  
            await channel.send(getBattleRules())
            t = TIME_LIMIT*60
            mins, secs = divmod(t, 60) 
            timer = "**Teambuilding: {:02d}:{:02d}**".format(mins, secs)
            timerMessage = await channel.send(timer)
            while t: 
                if (not battleInProgress): break
                time.sleep(1)
                t -= 1
                mins, secs = divmod(t, 60) 
                timer = "**Teambuilding: {:02d}:{:02d}**".format(mins, secs)
                await timerMessage.edit(content=timer)
            await timerMessage.delete()
            battleInProgress = False
    elif message.content == "!stop":
        channel = client.get_channel(int(os.getenv("MAIN_CHANNEL")))
        await channel.send("Battle stopped.")
        battleInProgress = False
    elif message.content == "!purge":
        channel = client.get_channel(int(os.getenv("BATTLE_CHANNEL")))
        async for mes in channel.history():
            await mes.delete()
        channel = client.get_channel(int(os.getenv("MAIN_CHANNEL")))
        await channel.send("All battles removed.")
client.run(TOKEN)
