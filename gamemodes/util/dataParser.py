import shutil
import tempfile
import urllib.request

import pokebase as pb
import json

with urllib.request.urlopen('https://raw.githubusercontent.com/smogon/pokemon-showdown/master/data/pokedex.ts') as response:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        shutil.copyfileobj(response, tmp_file)

delLine = False
with open(tmp_file.name) as html:
  lines = html.read().splitlines()
  fw = open("gamemodes\\util\\data\\monData.py", "w")
  fw.write("monData = {\n")
  previous = "*"
  for line in lines[1:-1]:
    if line == "\t\t\'" or line == "\t\t" or "//" in line: continue
    if "G-Max Volt Crash" in line: delLine = False
    if delLine:
        if line == "\t\t],":
            delLine = False 
        continue
    if "evos: [\"Raichu\", \"Raichu-Alola\"]" in line or "[\"Vivillon-Archipelago\", \"Vivillon-Continental\"" in line or "[\"Furfrou-Dandy\", \"Furfrou-Debutante\"" in line or "prevo: \"Type: Null\"" in line or "cosmeticFormes: [\"Minior-Orange\", \"Minior-Yellow\"" in line: 
        delLine = True
    elif "Arceus-Fighting" in line and "Arceus-Poison" in line or "missingno" in line:
        delLine = True
        continue
    if not line.startswith('\t\t') and not line.startswith('\t}'):
      line = "\t" + line.lstrip().capitalize()
    line = line.replace("\"", "\'")
    line = line.replace(":", "\':")
    line = line.replace("M\':", "\"M\":")
    line = line.replace("F\':", "\"F\":")
    line = line.replace("hp\':", "\"HP\":")
    line = line.replace("atk\':", "\"Atk\":")
    line = line.replace("def\':", "\"Def\":")
    line = line.replace("spa\':", "\"SpA\":")
    line = line.replace("spd\':", "\"SpD\":")
    line = line.replace("spe\':", "\"Spe\":")
    line = line.replace("0\':", "\"0\":")
    line = line.replace("1\':", "\"1\":")
    line = line.replace("H\':", "\"H\":")
    line = line.replace("S\':", "\"S\":")
    line = line.replace ("\'\'", "\'")
    line = line.replace ("1\"0\":", "10\':")
    line = line.replace ("Pa\'u", "Pa\\'u")
    line = line.replace ("Type\': Null", "Type: Null")
    line = line.replace ("Dragon's Maw", "Dragon\\'s Maw")
    line = line.replace ("Mind's Eye", "Mind\\'s Eye")

    if line.startswith('\t\t'):
      if "evoItem" in line or "evoType" in line or "evoCondition" in line or "eggGroups" in line or "otherFormes" in line or "formeOrder" in line or "canHatch" in line or "cannotDynamax" in line: continue
      fw.write('\t\t\'')
    else:
      if line.startswith('\t}'):
        fw.write('\t')
      else:
        if line.lstrip().startswith(previous):
          index = len(previous)+1
          # line = line[:index] + "-" + line[index:].capitalize()
        else:
          previous = line[:line.find("\'")].lstrip()
        fw.write('\t\'')
    fw.write(line.lstrip() + "\n")
  fw.write("}\n")

with urllib.request.urlopen('https://raw.githubusercontent.com/smogon/pokemon-showdown/master/data/formats-data.ts') as response:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        shutil.copyfileobj(response, tmp_file)

with open(tmp_file.name) as html:
  lines = html.read().splitlines()
  fw.write("\ntierData = {\n")
  previous = "*"
  for line in lines[1:-1]:
    if not line.startswith('\t\t') and not line.startswith('\t}'):
      line = "\t" + line.lstrip().capitalize()
    line = line.replace("\"", "\'")
    line = line.replace(":", "\':")
    line = line.replace("Uber", "Ubers")
    
    line = line.replace("AG", "Illegal")
    line = line.replace("UUBL", "OU")
    line = line.replace("RUBL", "UU")
    line = line.replace("NUBL", "RU")
    line = line.replace("PUBL", "NU")
    line = line.replace("ZUBL", "PU")
    line = line.replace("(OU)", "OU")
    
    deez = line.find('//')
    if deez != -1:
      line = line[:deez]

    if line.startswith('\t\t'):
      fw.write('\t\t\'')
    else:
      if line.startswith('\t}'):
        fw.write('\t')
      else:
        if line.lstrip().startswith(previous):
          index = len(previous)+1
          # line = line[:index] + "-" + line[index:].capitalize()
        else:
          previous = line[:line.find("\'")].lstrip()
        fw.write('\t\'')

    fw.write(line.lstrip() + "\n")

  fw.write("}")

fw.close()

from data.monData import tierData, monData

mons = {}
for key, value in monData.items():
    mons[key] = value

for key, value in tierData.items():
    if key in mons:
        mons[key].update(value)
    else:
        mons[key] = value

mons = {k: v for k, v in mons.items() if 'name' in v}
mons = {v['name']: {**v, 'name': v['name']} for k, v in mons.items()}
for key in mons:
    del mons[key]['name']
fw = open("gamemodes\\util\\data\\monData.py", "w")
fw.write(f'monData = {json.dumps(mons, indent=4)}\n')
fw.close()

"""
fw = open("gamemodes\\util\\data\\moveNames.py", "w")
fw.write("moveList = [")
i = 1
fw.write("\"" + str(pb.move(id_or_name=i)).replace("-", " ").title() + "\"")
while i > 0:
  i += 1
  try:
    m = pb.move(id_or_name=i)
  except:
    break
  fw.write(",\"" + str(m).replace("-", " ").title() + "\"")
fw.write("]")

fw = open("gamemodes\\util\\data\\abilityNames.py", "w")
fw.write("abilityList = [")
i = 1
fw.write("\"" + str(pb.ability(id_or_name=i)).replace("-", " ").title() + "\"")
while i > 0:
  i += 1
  try:
    m = pb.ability(id_or_name=i)
  except:
    break
  fw.write(",\"" + str(m).replace("-", " ").title() + "\"")
fw.write("]")
"""