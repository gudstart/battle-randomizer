import random as rand
import string
import time
from numpy.random import randint

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

rules = [
    {"Only mons starting with @": 10},
    {"Only moves starting with @": 10},
    {"Only items starting with @": 10},
    {
        "Only mons that have 1 type": 5,
        "Only mons that are part & type": 10
    },
    {"Damaging moves can only be up to # base power": 10},
    {"No STAB moves allowed (Tera type included if terastallized)": 0},
    {"* stat has to be max !": 10}
]

#LISTS
types = ["Normal", "Fire", "Water", "Grass", "Electric", "Ice", "Fighting", "Poison", 
         "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy"]
tiers = ["LC", "ZU", "NU", "PU", "RU", "UU", "OU", "Ubers"]
stats = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]

#### CLAUSES ####
print(NUM_MONS, "MONS,", TIME_LIMIT, "MINUTE TIME LIMIT")
print("NATIONAL DEX")         if randint(100) <= SETTING_NATDEX_CHANCE else print("SV POKEDEX")
print("Only", rand.choice(tiers), "pokemon or below")
print("TERASTALLIZE ON") if randint(100) <= SETTING_TERASTALLIZE_ON_CHANCE else print("TERASTALLIZE OFF")
print()

print("Species Clause ON")    if randint(100) <= SPECIES_CLAUSE_ON_CHANCE else print("Species Clause OFF")    # Species Clause
print("Moody Clause ON")      if randint(100) <= MOODY_CLAUSE_ON_CHANCE else print("Moody Clause OFF")    # Moody Clause
print("OHKO Clause ON")       if randint(100) <= OHKO_CLAUSE_ON_CHANCE else print("OHKO Clause OFF")    # OHKO Clause
print("Evasion Clause ON")    if randint(100) <= EVASION_CLAUSE_ON_CHANCE else print("Evasion Clause OFF")    # Evasion Clause
if randint(100) <= ITEM_CLAUSE_ON_CHANCE: print("Item Clause ON (No 2 pokemon may have the same item)")    # Item Clause
print()

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
    statLowerBound = 40
    statUpperBound = 110
    selectedRuleString = selectedRuleString.replace("*", rand.choice(stats))
    selectedRuleString = selectedRuleString.replace("!", str(randint(RULE_MAX_STAT_RANGE[0]/5, RULE_MAX_STAT_RANGE[1]/5)*5))
    print("RULE " + str(i + 1) + ": " + selectedRuleString)

t = TIME_LIMIT*60
while t: 
        mins, secs = divmod(t, 60) 
        timer = '{:02d}:{:02d}'.format(mins, secs) 
        print(timer, end="\r") 
        time.sleep(1) 
        t -= 1