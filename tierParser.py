import shutil
import tempfile
import urllib.request

with urllib.request.urlopen('https://raw.githubusercontent.com/smogon/pokemon-showdown/master/data/formats-data.ts') as response:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        shutil.copyfileobj(response, tmp_file)

with open(tmp_file.name) as html:
  lines = html.read().splitlines()

  fw = open("monTiers.py", "w")
  fw.write("tierData = {\n")

  for line in lines[1:-1]:
    line = line.replace("\"", "\'")
    line = line.replace(":", "\':")

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
