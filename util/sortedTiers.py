from data.monTiers import tierData

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
    "Illegal": []
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
    "Illegal": []
}

for pokemon, data in tierData.items():
    if "natDexTier" in data:
        ndTiers[data["natDexTier"]].append(pokemon)
    if "tier" in data:
        tiers[data["tier"]].append(pokemon)

print(tiers["NU"])