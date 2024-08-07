import random as rand
from numpy.random import randint
from dotenv import load_dotenv
import pokebase as pb

from gamemodes.util.data.monTiers import tierData

#### SETTINGS ####
TIME_LIMIT_MINUTES = 15

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

def getDraftRules(format):
    ndSelection = {
        "OU": rand.sample(ndTiers["OU"], 4),
        "UU": rand.sample(ndTiers["UU"], 4),
        "RU": rand.sample(ndTiers["RU"], 4),
        "Tera Captains": rand.sample(ndTiers["NFE"], 4),
    }

    selection = {
        "OU": rand.sample(tiers["OU"], 4),
        "UU": rand.sample(tiers["UU"], 4),
        "RU": rand.sample(tiers["RU"], 4),
        "Tera Captains": rand.sample(tiers["NU"] + tiers["PU"] + tiers["ZU"], 4),
    }

    randN = randint(2)
    r = "## SNAKE DRAFT: YOUNGEST" if randN == 0 else "## SNAKE DRAFT: OLDEST"
    text = r + " GOES FIRST\n"
    text += "Only Tera Captains may terastallize. " + str(TIME_LIMIT_MINUTES) + " minute time limit. Run **!draft** again to start timer\n"
    text += "First pick: **OU** and below. Second pick: **UU** and below. Third pick: **RU** and below. Fourth pick: **Tera Captains** only.\n\n"
    text = text + "**NATIONAL DEX**\n" if format == "nd" else text + "**STANDARD DEX**\n"
    form = ndSelection if format == "nd" else selection
    for i in range (4):
        text += "**" + list(form.keys())[i]  + ":** "
        for j in list(form.values())[i]:
            text += j + ", "
        text = text[:-2]
        text += "\n"
    return text