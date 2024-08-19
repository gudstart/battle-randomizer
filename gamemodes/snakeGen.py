import random as rand
from numpy.random import randint
from dotenv import load_dotenv
import pokebase as pb

from gamemodes.util.data.monData import monData

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

for pokemon, data in monData.items():
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

    text = "# SNAKE\n"
    text += "## NATIONAL DEX: " if format == "nd" else "## STANDARD DEX: "
    text += "SNAKE DRAFT, YOUNGEST" if randint(2) == 0 else "SNAKE DRAFT, OLDEST"
    text += " GOES FIRST\n"
    text += "Only Tera Captains may terastallize. " + str(TIME_LIMIT_MINUTES) + " minute teambuilding time limit. Run **!snake** again to start timer\n"
    text += "First pick: **OU** and below. Second pick: **UU** and below. Third pick: **RU** and below. Fourth pick: **Tera Captains** only.\n\n"
    form = ndSelection if format == "nd" else selection
    for i in range (4):
        text += "**" + list(form.keys())[i]  + ":** "
        for j in list(form.values())[i]:
            text += j + ", "
        text = text[:-2]
        text += "\n"
    
    text += "[Pokemon Showdown Teambuilder](https://play.pokemonshowdown.com/teambuilder)\n"
    return text