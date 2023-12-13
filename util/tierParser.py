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

  for line in lines[1:-1]:
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
        fw.write('\t\'')

    fw.write(line.lstrip() + "\n")

  fw.write("}")