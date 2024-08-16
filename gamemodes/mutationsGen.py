import requests
import random as rand

from gamemodes.util.data.monTiers import tierData

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

print(rand.choice(tiers))

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
