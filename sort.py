import json

with open("esports-data/tournaments.json", "r") as json_file:
    tournaments_data = json.load(json_file)

f = open("sort.json", "w")
lines =[]

for tournament in tournaments_data:
    lines.append(tournament)

lines = sorted(lines, key=lambda k: k['startDate'])
f.write('[')
for line in lines:
    f.write(json.dumps(line))
    f.write(",\n")
f.write(']')

f.close()
