import csv
ref_dict = {}
current_dict = {}
with open("games.csv", "r") as csv_file:
    game_data = csv.reader(csv_file)
    start = True
    for line in game_data:
        if start:
            currentStage= line[4]
            start = False
        if line[4] == currentStage:
            if line[5] in current_dict.keys():
                if line[7] in ref_dict.keys():
                    current_dict.update(line[5])