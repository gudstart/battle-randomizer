import re
import random as rand
import string
from numpy.random import randint
from dotenv import load_dotenv
import pokebase as pb

#### SETTINGS ####
NUM_RULES = 3
NUM_MONS = 3
TIME_LIMIT_MINUTES = 7
RULE_MAX_BP_RANGE = [50, 100]
RULE_MAX_STAT_RANGE = [40, 100]
SETTING_NATDEX_CHANCE = 50
SETTING_TERASTALLIZE_ON_CHANCE = 50

SPECIES_CLAUSE_ON_CHANCE = 90
MOODY_CLAUSE_ON_CHANCE = 60
OHKO_CLAUSE_ON_CHANCE = 85
EVASION_CLAUSE_ON_CHANCE = 80
ITEM_CLAUSE_ON_CHANCE = 50
TRAPPING_CLAUSE_ON_CHANCE = 70

#### RULESET ####
# List of dictionaries representing categories of rules.
# Value of dictionary indicates how much weight is given to that rule when randomly selecting
# If a rule from a category is selected, the other rules from that category can no longer be selected for further rules.

ruleset = [
    
    #POKEMON RULES
    {
        "Only mons starting with **@**": 10,
        "Only mons that have the following abilities: **^**, **^** or **^** (Their other abilities may also be used)": 10,
        "Only mons with less than an 8 letter name": 3,
        "Only mons with an 8 or more letter name": 3,
        "Only mons that have **1** type": 5,
        "Only mons that are part **&** type": 10
    },
    
    #MOVE RULES
    {
        "Only moves starting with **@**": 14,
        "Only moves that have 1 word": 3,
        "Only moves that have 2 words": 3
    },
    
    #ITEM RULES
    {
        "Only items starting with **@**": 5,
        "Only **gems** allowed as items": 5,
        "Only **berries** allowed as items": 5,
        "Only **plates** allowed as items": 5,
        "Only **Z items** allowed as items": 5
    },
    
    #HACKMON RULES
    {"Regardless of other rules, all mons have access to the move **$**": 15},
    {"Regardless of other rules, all mons have access to any move that starts with **@**": 5},
    {"Regardless of other rules, all mons have access to the ability **^**": 15},
    {"Regardless of other rules, all mons have access to any ability that starts with **@**": 5},
    {"All mons may use up to 1 of ANY existing **&** type move including their own": 15},
    
    #NATURE RULES
    {"Your mons must have the **%** nature": 5},
    
    #OTHER RULES
    {"Damaging moves can only be up to **#** base power. Multihit moves can only be up to **`** base power.": 10},
    {"No STAB moves allowed (Tera type included if terastallized)": 2},
    {"All mons must not surpass a base | stat of **!**": 10}
]

#LISTS
types = ["Normal", "Fire", "Water", "Grass", "Electric", "Ice", "Fighting", "Poison", 
         "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy"]
SV_tiers = ["LC", "ZU", "NU", "PU", "RU", "UU", "OU", "Ubers"]
NATDEX_tiers = ["LC", "PFE", "RU", "UU", "OU", "Ubers"]
stats = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]
influential_natures = ["Lonely", "Adamant", "Naughty", "Brave", "Bold", "Impish", "Lax", "Relaxed", "Modest", "Bashful", "Rash", "Quiet", "Calm", "Gentle", "Careful", "Sassy", "Timid", "Hasty", "Jolly", "Naive"]
numMoves = 904 #We use pokebase api for moves
numAbilities = 303 #We use pokebase api for abilities

def getBattleRules():
    global ruleset
    rules = ruleset
    
    #### CLAUSES ####
    battleRules = "## " + str(NUM_MONS) + " MONS, " + str(TIME_LIMIT_MINUTES) + " MINUTE TIME LIMIT\n"
    if randint(100) <= SETTING_NATDEX_CHANCE:
        battleRules += "**NATIONAL DEX**\n"
        battleRules += "Only **" + rand.choice(NATDEX_tiers) + "** pokemon or below\n"
    else:
        battleRules += "**SV DEX**\n"
        battleRules += "Only **" + rand.choice(SV_tiers) + "** pokemon or below\n"
    
    battleRules += "TERASTALLIZE **ON**\n\n" if randint(100) <= SETTING_TERASTALLIZE_ON_CHANCE else "TERASTALLIZE **OFF**\n\n"

    battleRules += "Species Clause ON\n"    if randint(100) <= SPECIES_CLAUSE_ON_CHANCE else "Species Clause **OFF** (More than 1 of the same species may be used)\n"
    battleRules += "Moody Clause ON\n"      if randint(100) <= MOODY_CLAUSE_ON_CHANCE else "Moody Clause **OFF** (The ability Moody is allowed)\n"
    battleRules += "OHKO Clause ON\n"       if randint(100) <= OHKO_CLAUSE_ON_CHANCE else "OHKO Clause **OFF** (OHKO moves are allowed)\n"
    battleRules += "Evasion Clause ON\n"    if randint(100) <= EVASION_CLAUSE_ON_CHANCE else "Evasion Clause **OFF** (Evasion moves are allowed)\n"
    battleRules += "Trapping Clause ON\n"    if randint(100) <= TRAPPING_CLAUSE_ON_CHANCE else "Trapping Clause **OFF** (Trapping moves and abilities are allowed)\n"
    if randint(100) <= ITEM_CLAUSE_ON_CHANCE: battleRules += "Item Clause **ON** (No 2 pokemon may have the same item)\n"
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
        bpRuleNum = randint(RULE_MAX_BP_RANGE[0]/5, RULE_MAX_BP_RANGE[1]/5)*5
        selectedRuleString = selectedRuleString.replace("#", str(bpRuleNum)).replace("`", str(int(round(bpRuleNum/5+10))))
        selectedRuleString = selectedRuleString.replace("|", rand.choice(stats))
        selectedRuleString = selectedRuleString.replace("!", str(randint(RULE_MAX_STAT_RANGE[0]/5, RULE_MAX_STAT_RANGE[1]/5)*5))
        if selectedRuleString.find("$"): #Minimize need for API call
            selectedRuleString = selectedRuleString.replace("$", str(pb.move(randint(1, numMoves))).replace("-", " ").title())
        selectedRuleString = selectedRuleString.replace("%", rand.choice(influential_natures))
        if selectedRuleString.find("^"): #Minimize need for API call
            selectedRuleString = re.sub(r'\^', lambda x: str(pb.ability(randint(1, numAbilities))).replace("-", " ").title(), selectedRuleString)
        battleRules += "- " + selectedRuleString + "\n"
    
    battleRules += "[Teambuilder](https://play.pokemonshowdown.com/teambuilder)\n"
    return battleRules
