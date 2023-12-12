import re
import random as rand
import string
from numpy.random import randint
from dotenv import load_dotenv
import pokebase as pb

from monTiers import tierData

#### SETTINGS ####

Ubers = []
OU = []
UU = []
RU = []
NFE = []
LC = []

for pokemon, data in tierData.items():
  tier = ""

  if "natDexTier" in data:
    tier = data["natDexTier"]
  elif "tier" in data:
    tier = data["tier"]
  else:
    tier = "isNonestandard"

  if tier == "Uber":
    Ubers.append(pokemon)
  elif tier == "OU":
    OU.append(pokemon)
  elif tier == "UU":
    UU.append(pokemon)
  elif tier == "RU":
    RU.append(pokemon)
  elif tier == "NFE":
    NFE.append(pokemon)
  elif tier == "LC":
    LC.append(pokemon)