import random as rand
import numpy as np
import string

randin = np.random.randint
print(randin(50))
#### SETTINGS ####
NUM_RULES = 3
NUM_MONS = 3
TIME_LIMIT = 7
RULE_MAX_BP_RANGE = [50, 130]
RULE_MAX_STAT_RANGE = [40, 100]

SETTING_NATDEX_CHANCE = 50
SETTING_TERASTALLIZE_CHANCE = 50

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
print(NUM_MONS, " MONS, ", TIME_LIMIT," MINUTE TIME LIMIT")
print("NATIONAL DEX")         if randint(100) <= NAT else print("SV POKEDEX")            # Dex Picker
print("Only", rand.choice(tiers), "pokemon or below")                                # Tier Picker
print("TERASTALLIZE ON") if randint(100) <=  else print("TERASTALLIZE OFF")
print()

print("Species Clause ON")    if randint(100) <= 90 else print("Species Clause OFF")    # Species Clause
print("Moody Clause ON")      if randint(100) <= 70 else print("Moody Clause OFF")    # Moody Clause
print("OHKO Clause ON")       if randint(100) <= 85 else print("OHKO Clause OFF")    # OHKO Clause
print("Evasion Clause ON")    if randint(100) <= 85 else print("Evasion Clause OFF")    # Evasion Clause
if randint(100) > 50: print("Item Clause ON (No 2 pokemon may have the same item)")    # Item Clause
print()

#### SELECTED RULES ####
for i in range(NUM_RULES):
    selectedRules = [(key value) for rule, weight, selected in rules if selected == True]
    randNum = randint(np.sum([t[1] for t in selectedRules]))

    selectedRule = 0
    for t in selectedRules:
        selectedRule = selectedRule + t[1]
        if selectedRule >= randNum:
            selectedRule = t
            break
    delInd = rules.index(selectedRule)
    del rules[delInd]
    selectedRuleString = selectedRule[0].replace("@", rand.choice(string.ascii_letters).upper())
    selectedRuleString = selectedRuleString.replace("&", rand.choice(types))
    bpLowerBound = 50
    bpUpperBound = 130
    selectedRuleString = selectedRuleString.replace("#", str(randint(bpLowerBound/5, bpUpperBound/5)*5))
    statLowerBound = 40
    statUpperBound = 110
    selectedRuleString = selectedRuleString.replace("*", rand.choice(stats))
    selectedRuleString = selectedRuleString.replace("!", str(randint(statLowerBound/5, statUpperBound/5)*5))
    print("RULE " + str(i + 1) + ": " + selectedRuleString)
