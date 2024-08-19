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
  fw = open("gamemodes\\util\\data\\monData.py", "w", encoding="utf-8")
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
fw = open("gamemodes\\util\\data\\monData.py", "w", encoding="utf-8")
fw.write(f'monData = {json.dumps(mons, indent=4)}\n')
fw.close()

with urllib.request.urlopen('https://raw.githubusercontent.com/smogon/pokemon-showdown/master/data/moves.ts') as response:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        shutil.copyfileobj(response, tmp_file)

with open(tmp_file.name) as html:
  lines = html.read().splitlines()
  fw = open("gamemodes\\util\\data\\moveData.py", "w", encoding="utf-8")
  fw.write("moveData = {\n")
  previous = "*"
  for line in lines[3:-1]:
    if "//" in line or line == "": continue
    if not line.startswith('\t\t') and not line.startswith('\t}'):
      line = line.replace("\"", "")
      line = "\t" + line.lstrip().capitalize()
    line = line.replace("\"", "\'")
    line = line.replace(":", "\':")
    line = line.replace("true", "100")
    line = line.replace("false", "0")
    line = line.replace("null", "None")
    line = line.replace("'s ", "\\'s ")
    deez = line.find('//')
    if deez != -1:
      line = line[:deez]

    if line.startswith('\t\t'):
      if 'anyAirborne' in line or 'defender' in line or 'attacker' in line or 'case ' in line or 'rolloutData' in line or 'showMsg' in line or 'factor' in line or 'move =' in line or 'default' in line or 'result' in line or 'message' in line or 'already' in line or 'action' in line or '\'stomp\'' in line or 'newMove' in line or 'onSource' in line or 'hasLast' in line or 'break' in line or 'duration' in line or 'iceballData' in line or 'bp *' in line or 'Hazard' in line or 'applies' in line or 'moveSlot' in line or '{' in line or 'secondar' in line or 'bp =' in line or 'moveData' in line or '\'mist\'' in line or '\'spikes\'' in line or ']' in line or 'success' in line or 'fail' in line or 'contact' in line or 'newType' in line or 'protect\':' in line or '\'\'' in line or "flags\':" in line or 'condition' in line or 'onResidual' in line or 'moveid' in line or 'onUpdate' in line or 'remove' in line or 'onEnd' in line or 'onTry' in line or 'onModify' in line or 'move.type' in line or 'onSide' in line or 'pokemon' in line or ')' in line or 'move.' in line or 'source' in line or 'as ID' in line or 'secondary\':' in line or 'atk\':' in line or 'spe\':' in line or 'def\':' in line or 'spa\':' in line or 'spd\':' in line or '}' in line or 'boost' in line or 'stat' in line or 'if (' in line or 'basePowerCallback' in line or 'debug' in line or 'return' in line or 'BoostID' in line or 'onHit' in line or 'const ' in line or 'for (' in line or 'this.' in line or 'target' in line or 'onPrepareHit' in line or 'onStart' in line or 'onRestart' in line or 'delete' in line or 'let ' in line or 'ally' in line or 'continue' in line or 'self' in line: 
        continue
      fw.write('\t\t\'')
    else:
      if line.startswith('\t}'):
        fw.write('\t')
      else:
        if line.lstrip().startswith(previous):
          index = len(previous)+1
        else:
          previous = line[:line.find("\'")].lstrip()
        fw.write('\t\'')
        
    fw.write(line.lstrip() + "\n")
    

  fw.write("}")

fw.close()

from data.moveData import moveData

moves = {}
moves = {k: v for k, v in moveData.items() if 'name' in v}
moves = {v['name']: {**v, 'name': v['name']} for k, v in moves.items()}
for key in moves:
    del moves[key]['name']
fw = open("gamemodes\\util\\data\\moveData.py", "w", encoding="utf-8")
fw.write(f'moveData = {json.dumps(moves, indent=4)}\n')
fw.close()

with urllib.request.urlopen('https://raw.githubusercontent.com/smogon/pokemon-showdown/master/data/abilities.ts') as response:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        shutil.copyfileobj(response, tmp_file)

with open(tmp_file.name) as html:
  lines = html.read().splitlines()
  fw = open("gamemodes\\util\\data\\abilityData.py", "w", encoding="utf-8")
  fw.write("abilityData = {\n")
  previous = "*"
  for line in lines[42:-1]:
    if "//" in line or line == "": continue
    if not line.startswith('\t\t') and not line.startswith('\t}'):
      line = line.replace("\"", "")
      line = "\t" + line.lstrip().capitalize()
    line = line.replace("\"", "\'")
    line = line.replace(":", "\':")
    line = line.replace("true", "100")
    line = line.replace("false", "0")
    line = line.replace("null", "None")
    line = line.replace("'s ", "\\'s ")
    deez = line.find('//')
    if deez != -1:
      line = line[:deez]

    if line.startswith('\t\t'):
      if 'activated' in line or '++' in line or 'pkmn' in line or 'announced' in line or 'Berry' in line or '&&' in line or 'active.' in line or 'warn' in line or 'berry' in line or 'judgment' in line or 'anyAirborne' in line or 'defender' in line or 'attacker' in line or 'case ' in line or 'rolloutData' in line or 'showMsg' in line or 'factor' in line or 'move =' in line or 'default' in line or 'result' in line or 'message' in line or 'already' in line or 'action' in line or '\'stomp\'' in line or 'newMove' in line or 'onSource' in line or 'hasLast' in line or 'break' in line or 'duration' in line or 'iceballData' in line or 'bp *' in line or 'Hazard' in line or 'applies' in line or 'moveSlot' in line or '{' in line or 'secondar' in line or 'bp =' in line or 'moveData' in line or '\'mist\'' in line or '\'spikes\'' in line or ']' in line or 'success' in line or 'fail' in line or 'contact' in line or 'newType' in line or 'protect\':' in line or '\'\'' in line or "flags\':" in line or 'condition' in line or 'onResidual' in line or 'moveid' in line or 'onUpdate' in line or 'remove' in line or 'onEnd' in line or 'onTry' in line or 'onModify' in line or 'move.type' in line or 'onSide' in line or 'pokemon' in line or ')' in line or 'move.' in line or 'source' in line or 'as ID' in line or 'secondary\':' in line or 'atk\':' in line or 'spe\':' in line or 'def\':' in line or 'spa\':' in line or 'spd\':' in line or '}' in line or 'boost' in line or 'stat' in line or 'if (' in line or 'basePowerCallback' in line or 'debug' in line or 'return' in line or 'BoostID' in line or 'onHit' in line or 'const ' in line or 'for (' in line or 'this.' in line or 'target' in line or 'onPrepareHit' in line or 'onStart' in line or 'onRestart' in line or 'delete' in line or 'let ' in line or 'ally' in line or 'continue' in line or 'self' in line: 
        continue
      fw.write('\t\t\'')
    else:
      if line.startswith('\t}'):
        fw.write('\t')
      else:
        if line.lstrip().startswith(previous):
          index = len(previous)+1
        else:
          previous = line[:line.find("\'")].lstrip()
        fw.write('\t\'')
        
    fw.write(line.lstrip() + "\n")
    

  fw.write("}")

fw.close()

from data.abilityData import abilityData

abilities = {}
abilities = {k: v for k, v in abilityData.items() if 'name' in v}
abilities = {v['name']: {**v, 'name': v['name']} for k, v in abilities.items()}
for key in abilities:
    del abilities[key]['name']
fw = open("gamemodes\\util\\data\\abilityData.py", "w", encoding="utf-8")
fw.write(f'abilityData = {json.dumps(abilities, indent=4)}\n')
fw.close()