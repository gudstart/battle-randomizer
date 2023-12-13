import shutil
import tempfile
import urllib.request

with urllib.request.urlopen('https://raw.githubusercontent.com/smogon/pokemon-showdown/master/data/formats-data.ts') as response:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        shutil.copyfileobj(response, tmp_file)

with open(tmp_file.name) as html:
  lines = html.read().splitlines()

  fw = open("util\\data\\monTiers.py", "w")
  fw.write("tierData = {\n")
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
          line = line[:index] + "-" + line[index:].capitalize()
        else:
          previous = line[:line.find("\'")].lstrip()
          for l in [g for g in lines if not g.startswith('\t\t') and not g.startswith('\t}')][1:]:
            if line.lstrip()[:line.lstrip().find("\'")].lower().endswith("f") and l[1:l.find(":")].lower().endswith("m") and line.lstrip()[:line.lstrip().find("\'")][:-1].lower() == l[1:l.find(":")].lower()[:-1]:
              index = line.lower().rfind("f")
              line = line[:index] + "-" + line[index:].capitalize()
              break
            if line.lstrip()[:line.lstrip().find("\'")].lower().endswith("m") and l[1:l.find(":")].lower().endswith("f") and line.lstrip()[:line.lstrip().find("\'")][:-1].lower() == l[1:l.find(":")].lower()[:-1]:
              index = line.lower().rfind("m")
              line = line[:index] + "-" + line[index:].capitalize()
              break
        line = line.replace("totem", "-Totem")
        line = line.replace("Megax", "Mega-X")
        line = line.replace("Megay", "Mega-Y")
        line = line.replace("Dawnwings", "Dawn-Wings")
        line = line.replace("Duskmane", "Dusk-Mane")
        if line.lstrip().startswith("Tapu"):
          line = line[:5] + "-" + line[5:].capitalize()
        fw.write('\t\'')

    fw.write(line.lstrip() + "\n")

  fw.write("}")