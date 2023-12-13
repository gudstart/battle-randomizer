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
  tier = ""

  if "natDexTier" in data:
    ndTiers[data["natDexTier"]].append(pokemon)
  if "tier" in data:
    tiers[data["tier"]].append(pokemon)

for t in tiers:
    tiers[t] = [n.capitalize() for n in tiers[t]]
    previous = "*"
    for i in range(len(tiers[t])):
        if tiers[t][i].startswith(previous):
            index = len(previous)
            tiers[t][i] = tiers[t][i][:index] + "-" + tiers[t][i][index:].capitalize()
        else:
            previous = tiers[t][i]

print(tiers["NU"])