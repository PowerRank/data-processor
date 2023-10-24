import csv
import glicko2
import datetime
import json

def addRankInfo(line, team, opponent):
    if line[team] not in current_dict.keys():
        current_dict[line[team]] = [[],[],[]]
    if line[opponent] in ref_dict.keys():
        current_dict[line[team]][0].append(ref_dict[line[opponent]][0])
        current_dict[line[team]][1].append(ref_dict[line[opponent]][1])
    else:
        current_dict[line[team]][0].append(1500)
        current_dict[line[team]][1].append(350)
    outcome = 0
    if line[team+1] == 'win':
        outcome = 1
    current_dict[line[team]][2].append(outcome)

ref_dict = {}
current_dict = {}
vol_dict = {}
BONUS = 20
STAGEBONUS = 5
LEAGUEBONUS = 15
today = datetime.date.today()
#delta = datetime.timedelta(days=183) # ~ 6 months
delta = datetime.timedelta(days=300)
thatDay = today - delta
count = 0
stage_counter = 0

with open("games.csv", "r") as csv_file:
    game_data = csv.reader(csv_file)
    start = True 
    for line in game_data:
        if thatDay<(datetime.datetime.strptime(line[2], '%Y-%m-%d')).date():
            if start:
                currentStage= line[4]
                currentTournament = line[3]
                currentLeague = line[0]
                start = False
                stage_counter = 0
            count = 1
            addRankInfo(line, 5, 7)
            addRankInfo(line, 7, 5)
            count = 0
            currentStage = line[4]
            if currentTournament == line[3]:
                stage_counter = stage_counter +1
            currentTournament = line[3]
            for team in current_dict:
                print(current_dict[team][2])
                if team in ref_dict.keys():
                    teamObj = glicko2.Player(ref_dict[team][0], ref_dict[team][1], ref_dict[team][2])
                else:
                    teamObj = glicko2.Player()
                bonus = 0
                if currentLeague == 'Worlds' or currentLeague == 'MSI':
                    for outcome in current_dict[team][2]:
                        bonus = bonus + outcome
                elif currentLeague == 'LPL' or currentLeague == 'LCK':
                    for outcome in current_dict[team][2]:
                        bonus = bonus + outcome
                    bonus = bonus * LEAGUEBONUS* 3
                elif currentLeague == 'LEC':
                    for outcome in current_dict[team][2]:
                        bonus = bonus + outcome
                    bonus = bonus * LEAGUEBONUS* 2
                elif currentLeague == 'LCS':
                    for outcome in current_dict[team][2]:
                        bonus = bonus + outcome
                    bonus = bonus * LEAGUEBONUS
                bonus = bonus+(stage_counter*STAGEBONUS)
                teamObj.update_player([rating for rating in current_dict[team][0]], [rd for rd in current_dict[team][1]], current_dict[team][2])
                ref_dict[team] = [(teamObj.rating), teamObj.rd, teamObj.vol]
                vola = teamObj.vol
                if team not in vol_dict.keys():
                    vol_dict[team] = []
                vol_dict[team].append(vola)
                current_dict ={}
                currentLeague = line[0]

    for thing in ref_dict:
        print(thing, end=', ')
        print(ref_dict[thing])
       # print(vol_dict[thing])


with open("esports-data/teams.json", "r") as json_file:
    teams_data = json.load(json_file)
result = sorted(ref_dict.items(), key =(lambda x:x[1][0]), reverse=True)
f = open("ranks.csv", "w")
for rank in result:
    for i in teams_data:
        name = ''
        if i['team_id'] == rank[0]:
            name = i['name']
            break
    f.write(rank[0]+ ", " +name+" ,"+str(rank[1][0])+ "\n")
f.close()
    