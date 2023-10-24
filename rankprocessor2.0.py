import csv
import glicko2
import datetime
import json
import boto3

referenceDictionary = {}

today = datetime.date.today()
#delta = datetime.timedelta(days=183) # ~ 6 months
delta = datetime.timedelta(days=300)
thatDay = today - delta

WORLDBONUS = 20
LEAGUEBONUS = 7

start = True

def updateTeam(line, team, opponent):
    outcome = 0
    bonus = 0
    if line[team+1] == 'win':
        outcome = 1
        if line[0] == 'Worlds' or line[0] == 'MSI':
            bonus = bonus + WORLDBONUS
        elif line[0] == 'LPL' or line[0] == 'LCK':
            bonus = bonus + (LEAGUEBONUS* 3)
        elif line[0] == 'LEC':
            bonus = bonus + (LEAGUEBONUS* 2)
        elif line[0] == 'LCS':
            bonus = bonus + LEAGUEBONUS 
    if line[team] in referenceDictionary.keys():
        teamObject = glicko2.Player(referenceDictionary[line[team]][0], referenceDictionary[line[team]][1], referenceDictionary[line[team]][2])
        bonus = referenceDictionary[line[team]][3]+bonus
    else:
        teamObject = glicko2.Player()
    if line[opponent] in referenceDictionary.keys():
        teamObject.update_player([rating for rating in [referenceDictionary[line[opponent]][0]]], [rd for rd in [referenceDictionary[line[opponent]][1]]], [outcome])
    else:
        teamObject.update_player([rating for rating in [1500]], [ratingDeviation for ratingDeviation in [350]], [outcome])
    return teamObject, bonus


with open("games.csv", "r") as csv_file:
    game_data = csv.reader(csv_file)

    for line in game_data:
        if thatDay<(datetime.datetime.strptime(line[2], '%Y-%m-%d')).date():
            team1, bonus1 = updateTeam(line,5, 7)
            team2, bonus2 = updateTeam(line,5, 7)
            referenceDictionary[line[5]]= [team1.rating, team1.rd, team1.vol, bonus1]
            referenceDictionary[line[7]] = [team2.rating,team2.rd,team2.vol, bonus2]
    
for thing in referenceDictionary:
    print(thing, end=', ')
    print(referenceDictionary[thing])
    referenceDictionary[thing][0]= referenceDictionary[thing][0] + referenceDictionary[thing][3]

with open("esports-data/teams.json", "r") as json_file:
    teams_data = json.load(json_file)
result = sorted(referenceDictionary.items(), key =(lambda x:x[1][0]), reverse=True)
for rank in result:
    for i in teams_data:
        name = ''
        if i['team_id'] == rank[0]:
            name = i['name']
            break
    if name == '':
        continue
    print(rank[0]+ ", " +name+" ,"+str(int(rank[1][0]))+ "\n")

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Ratings')
count = 0
with table.batch_writer() as batch:
    for rank in result:
        for i in teams_data:
            name = ''
            if i['team_id'] == rank[0]:
                name = i['name']
                break
        if name == '':
            continue
        count = count +1
        batch.put_item(
            Item={
                'PK': 'Current',
                'SK': 'Team#' + rank[0],
                'Entity': 'Rank',
                'TeamId': rank[0],
                'Name': name,
                'Points': int(rank[1][0]),
                'Rank': str(count)
            }
        )

for thing in referenceDictionary:
    print(thing, end=', ')
    print(referenceDictionary[thing])