import requests
import random as rand

from util.data.monTiers import tierData

# Mutations
# 4 possible level mutations. Each mutation increases level from 100 by 5-20.
# 
mutationChance = {
    "Ubers": {
        "Level": 0,
        "EV": 5,
        "Move": 5,
        "Ability": 5
    },
    "OU": {
        "Level": 0,
        "EV": 5,
        "Move": 5,
        "Ability": 5
    },
    "UU": {
        "Level": 0,
        "EV": 5,
        "Move": 5,
        "Ability": 5
    },
    "RU": {
        "Level": 0,
        "EV": 5,
        "Move": 5,
        "Ability": 5
    },
    "NU": {
        "Level": 0,
        "EV": 5,
        "Move": 5,
        "Ability": 5
    },
    "PU": {
        "Level": 0,
        "EV": 5,
        "Move": 5,
        "Ability": 5
    },
    "ZU": {
        "Level": 0,
        "EV": 5,
        "Move": 5,
        "Ability": 5
    },
    "NFE": {
        "Level": 0,
        "EV": 5,
        "Move": 5,
        "Ability": 5
    },
    "LC": {
        "Level": 0,
        "EV": 5,
        "Move": 5,
        "Ability": 5
    }
}
tiers = {
    "Ubers": [],
    "OU": [],
    "UU": [],
    "RU": [],
    "NU": [],
    "PU": [],
    "ZU" : [],
    "NFE": [],
    "LC": [],
    "CAP": [],
    "CAP LC": [],
    "CAP NFE": [],
    "Illegal": [],
    "Unreleased": []
}

ndTiers = {
    "Ubers": [],
    "OU": [],
    "UU": [],
    "RU": [],
    "NU": [],
    "PU": [],
    "ZU" : [],
    "NFE": [],
    "LC": [],
    "Illegal": [],
    "Unreleased": []
}

for pokemon, data in tierData.items():
    if pokemon.find("-Totem") == -1 and pokemon.find("-Gmax") == -1:
        if "natDexTier" in data:
            ndTiers[data["natDexTier"]].append(pokemon)
        if "tier" in data:
            tiers[data["tier"]].append(pokemon)

del tiers["CAP LC"]
del tiers["CAP NFE"]
del tiers["CAP"]
del tiers["Illegal"]
del tiers["Unreleased"]
del ndTiers["Illegal"]
del ndTiers["Unreleased"]

tiers = {key:value for key, value in tiers.items() if value}
ndTiers = {key:value for key, value in ndTiers.items() if value}

def getMutationRules(format):
    form = ndTiers if format == "nd" else tiers
    print(form.keys())

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
        
getMutationRules("e")