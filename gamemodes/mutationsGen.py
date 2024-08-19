import requests
import random as rand
from numpy.random import randint

from gamemodes.util.data.monData import monData
from gamemodes.util.data.moveData import moveData
from gamemodes.util.data.abilityData import abilityData

#### SETTINGS ####
MONS_TO_SELECT = 3
TIME_LIMIT_MINUTES = 10
MONS_TO_SELECT_FROM = 8
SETTING_TERASTALLIZE_ON_CHANCE = 50

# Mutations {Type, Chance / 100}
# 4 possible level mutations. Each mutation increases level from 100 by n^2, where n is a random int on {1, 6}.
# 10 possible IV mutations. Each mutation starts by increasing a random stat from 31 by n^2, where n is a random int on {2, 10}, while having a 20% chance of moving to a different stat on the next mutation.
# 4 possible move mutations. Each mutation adds a random fixed move from the pool of all moves.
# 1 possible ability mutation. It will make the mon's ability a random n-5 star fixed ability from Showdown's 5 star rating system, where n is the min ability rating of the tier.

stats = ["HP", "Atk", "Def", "SpA", "SpD", "Spe"]

mutationChance = {
    "Ubers": {
        "Level": 0,
        "IV": 0,
        "Move": 5,
        "Ability": 5,
        "Min Ability Rating": 2
    },
    "OU": {
        "Level": 5,
        "IV": 5,
        "Move": 10,
        "Ability": 15,
        "Min Ability Rating": 2
    },
    "UU": {
        "Level": 10,
        "IV": 10,
        "Move": 15,
        "Ability": 20,
        "Min Ability Rating": 2.5
    },
    "RU": {
        "Level": 15,
        "IV": 15,
        "Move": 20,
        "Ability": 25,
        "Min Ability Rating": 3
    },
    "NU": {
        "Level": 20,
        "IV": 20,
        "Move": 25,
        "Ability": 30,
        "Min Ability Rating": 3.5
    },
    "PU": {
        "Level": 25,
        "IV": 25,
        "Move": 30,
        "Ability": 30,
        "Min Ability Rating": 4
    },
    "ZU": {
        "Level": 30,
        "IV": 30,
        "Move": 30,
        "Ability": 30,
        "Min Ability Rating": 4.5
    },
    "NFE": {
        "Level": 35,
        "IV": 35,
        "Move": 35,
        "Ability": 40,
        "Min Ability Rating": 5
    },
    "LC": {
        "Level": 40,
        "IV": 50,
        "Move": 50,
        "Ability": 50,
        "Min Ability Rating": 5
    }
}

def getMutationRules(format):
    text = "# MUTATIONS\n"
    text += "## NATIONAL DEX: " if format == "nd" else "## STANDARD DEX: "
    text += "DRAFT " + str(MONS_TO_SELECT) + " EACH, YOUNGEST" if randint(2) == 0 else "DRAFT " + str(MONS_TO_SELECT) + " EACH, OLDEST"
    text += " GOES FIRST\n"
    text += str(TIME_LIMIT_MINUTES) + " minute teambuilding time limit. Run **!mutations** again to start timer\n"
    text += "TERASTALLIZATION **ON**\n" if randint(100) <= SETTING_TERASTALLIZE_ON_CHANCE else "TERASTALLIZATION **OFF**\n"
    
    text += "OHKO / EVASION CLAUSE **ON** (MUTATIONS EXCEPTED)\n\n"
    
    noZ = {k:v for k, v in moveData.items() if "isZ" not in v and "isMax" not in v}
    
    tier = "natDexTier" if format == "nd" else "tier"
    form = {k:v for k, v in monData.items() if tier in v}
    form = {k:v for k, v in form.items() if v[tier] != "Illegal" and v[tier] != "Unreleased" and "CAP" not in v[tier]}
    
    pokeStr = ""
    
    for _ in range(MONS_TO_SELECT_FROM):
        mon, info = rand.choice(list(form.items()))
        mutInfo = mutationChance[info[tier]]
        
        level = 100
        for _ in range(4): 
            if randint(100)+1 <= mutInfo['Level']: level += (randint(6)+1)**2
        
        boostedStats = {
            "HP": 0, 
            "Atk": 0, 
            "Def": 0,
            "SpA": 0,
            "SpD": 0,
            "Spe": 0
        }
        
        '''
        index = rand.choice(list(boostedStats.keys()))
        for _ in range(10): 
            if randint(100)+1 <= mutInfo['IV']:
                boostedStats[index] += (randint(9)+2)**2
            if randint(100) < 20:
                existing = index
                while index == existing:
                    index = rand.choice(list(boostedStats.keys()))
        '''
        
        fixedMoves = []
        for _ in range(4):
            if randint(100)+1 <= mutInfo['Move']:
                fixedMoves.append(rand.choice(list(noZ.keys())))

        ability = ""
        if randint(100)+1 <= mutInfo['Ability']:
            ability = rand.choice([ability for ability, data in abilityData.items() if data.get("rating", 0) >= mutInfo['Min Ability Rating'] and "Zero to Hero" not in ability and "Power Construct" not in ability and "isNonstandard" not in data])
        
        pokeStr += writePokepaste(mon, level, boostedStats, fixedMoves, ability)
        del form[mon]
    
    pokeStr = postPokepaste(pokeStr)
    
    text += "**MUTATED MOVES / ABILITIES / IVS CANNOT BE MODIFIED.**\n\n"
    text += "[CREATE GEN 9 NATIONAL DEX UBERS TEAM THEN PASTE THIS LINK IN]" if format == "nd" else "[CREATE GEN 9 UBERS TEAM THEN PASTE THIS LINK IN]"
    text += "(" + pokeStr + ")\n\n"
    
    text += "[Pokemon Showdown Teambuilder](https://play.pokemonshowdown.com/teambuilder)\n"
    return text

def writePokepaste(name, level, IVs, move, ability):
    pokeStr = name + "\n"
    if ability != "": pokeStr += "Ability: " + ability + "\n"
    if level != 100: pokeStr += "Level: " + str(level) + "\n"
    if any(value != 0 for value in IVs.values()):
        pokeStr += "IVs: "
        ivStr = ""
        for k,v in IVs.items():
            if v != 0:
                ivStr += str(v + 31) + " " + k + " / "
        pokeStr += ivStr.rstrip(" / ") + "\n"
    if move:
        for i in range(len(move)):
            pokeStr += "- " + move[i] + "\n"
    pokeStr += "\n"
    return pokeStr

def postPokepaste(monSets):
        submit_url = "https://pokepast.es/create"
        data = {
            'paste': monSets,
            'name': 'Pokepaste',
            'visibility': 'unlisted'
        }
        response = requests.post(submit_url, data=data)
        if response.ok:
            pokepaste_link = response.url
            return pokepaste_link
        else:
            raise Exception("Failed to create Pokepaste.")