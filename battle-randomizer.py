import time
import os
import discord
from dotenv import load_dotenv

from gamemodes.scrambleGen import getBattleRules, TIME_LIMIT_MINUTES
from gamemodes.snakeGen import getDraftRules, TIME_LIMIT_MINUTES as DRAFT_TIME
battleInProgress = "None"

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
MAIN_CH = int(os.getenv("MAIN_CHANNEL"))
BATTLE_CH = int(os.getenv("BATTLE_CHANNEL"))
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
    if message.content.startswith ("!scramble"):
        if message.content != "!scramble" and message.content != "!scramble nd":
            channel = client.get_channel(MAIN_CH)
            await channel.send("Use !scramble for regular rule battle and !scramble nd for national dex rule battle!")
        else:
            if battleInProgress != "None":
                channel = client.get_channel(MAIN_CH)
                await channel.send("Battle already in progress!")
            else:
                channel = client.get_channel(BATTLE_CH)
                battleInProgress = "Battling"  
                await channel.send(getBattleRules("reg")) if message.content == "!scramble" else await channel.send(getBattleRules("nd"))
                t = TIME_LIMIT_MINUTES*60
                mins, secs = divmod(t, 60) 
                timer = "**Teambuilding: {:02d}:{:02d}**".format(mins, secs)
                timerMessage = await channel.send(timer)
                while t: 
                    if battleInProgress == "None": break
                    time.sleep(1)
                    t -= 1
                    mins, secs = divmod(t, 60) 
                    timer = "**Teambuilding: {:02d}:{:02d}**".format(mins, secs)
                    await timerMessage.edit(content=timer)
                await timerMessage.delete()
                battleInProgress = "None"
    elif message.content.startswith("!snake"):
        if message.content != "!snake" and message.content != "!snake nd":
            channel = client.get_channel(MAIN_CH)
            await channel.send("Use !snake for regular dex draft battle and !snake nd for national dex draft battle!")
        else:
            if battleInProgress == "Battling":
                channel = client.get_channel(MAIN_CH)
                await channel.send("Battle already in progress!")
            elif battleInProgress == "Drafting":
                channel = client.get_channel(BATTLE_CH)
                battleInProgress = "Battling"  
                t = DRAFT_TIME*60
                mins, secs = divmod(t, 60) 
                timer = "**Teambuilding: {:02d}:{:02d}**".format(mins, secs)
                timerMessage = await channel.send(timer)
                while t: 
                    if battleInProgress == "None": break
                    time.sleep(1)
                    t -= 1
                    mins, secs = divmod(t, 60) 
                    timer = "**Teambuilding: {:02d}:{:02d}**".format(mins, secs)
                    await timerMessage.edit(content=timer)
                await timerMessage.delete()
                battleInProgress = "None"
            else:
                channel = client.get_channel(BATTLE_CH)
                await channel.send(getDraftRules("reg")) if message.content == "!snake" else await channel.send(getDraftRules("nd"))
                battleInProgress = "Drafting"
    elif message.content == "!stop":
        channel = client.get_channel(MAIN_CH)
        await channel.send("Battle stopped.")
        battleInProgress = "None"
    elif message.content == "!help":
        channel = client.get_channel(MAIN_CH)
        await channel.send("Please refer to the #info channel to get started!")

client.run(TOKEN)
