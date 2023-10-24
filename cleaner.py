import json

leagues = ['LPL','LEC','LCK','LCS','PCS','VCS','CBLOL','LJL','LLA','Worlds','MSI']

with open("sort.json", "r") as json_file:
    tournaments_data = json.load(json_file)
with open("esports-data/leagues.json", "r") as json_file:
    leagues_data = json.load(json_file)

f = open("games.csv", "w")

for tournament in tournaments_data:

    for i in leagues_data:
        name=''
        if i['id'] == tournament["leagueId"]:
            name=i['name']
            break
    if name in leagues:
        for stage in tournament["stages"]:
            for section in stage["sections"]:
                for match in section["matches"]:
                    if match["state"] == "completed":
                        '''
                        If matches needed. Use the following.
                        f.write((name+","+tournament["startDate"]+","+tournament["endDate"]+","+tournament["id"] +"," +stage["name"]+","))
                        for team in match["teams"]:
                            f.write(team["id"]+","+team["result"]["outcome"]+",")
                        f.write("\n")
                        '''
                        for game in match["games"]:
                            if game["state"] != "unneeded":
                                f.write(name+","+tournament["startDate"]+","+tournament["endDate"]+","+tournament["id"] +"," +stage["name"]+",")
                                for team in game["teams"]:
                                    try:
                                        f.write(team["id"]+","+team["result"]["outcome"]+",")
                                    except TypeError:
                                        continue
                                f.write('\n')
                    else:
                        continue
f.close()
