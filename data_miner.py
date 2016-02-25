from bs4 import BeautifulSoup
from datetime import date
from operator import itemgetter
from lxml import html
import requests
import time
import sys
import datetime
import operator
import numpy as np

all_matrices = []

for period in range(1,122):
    r = requests.get('http://games.espn.go.com/fba/leaders?&scoringPeriodId=' + str(period) + '&seasonId=2016')
    soup = BeautifulSoup(r.text)
    t_r = soup.find("tr", attrs={"class":"playerTableBgRowSubhead tableSubHead"})
    rows = [t.get_text() for t in t_r.find_all("td")]
    print(rows)
    stats = ['PLAYER', '', 'OPP', 'STATUS', '', 'MIN', 'FGM/FGA', 'FG%', 'FTM/FTA', 'FT%', '3PM', 'REB', 'AST', 'STL', 'BLK', 'PTS']
    table = soup.find("table", attrs={"class":"playerTableTable tableBody"})
    game_data = {}
    player = ""
    index = 0
    real_index = 0
    for i in table.find_all("td"):
        if index > 1:
            ind = real_index % len(rows) 
            if ind == 0:
                print(str(real_index) + " " + i.get_text())
                player = i.get_text().split(",")[0].lower()
                if "*" in player:
                    player = player[:len(player)-1]
                game_data[player] = {}
            else:
                game_data[player][stats[ind]] = i.get_text()
            real_index += 1
        index += 1

    def createDataMatrix():
        # Creates Matrix A in Ax = B s.t. x is the weight vector,
        # and the rows of A are in the form [PTS, 3PM, REB, AST, STL, BLK]
        big_matrix = []
        for player in game_data.keys():
            if not player == 'player':
                if game_data[player]['PTS'] == '--':
                    return None
                else:
                    vector = [float(game_data[player]['PTS']), float(game_data[player]['3PM']), float(game_data[player]['REB']), float(game_data[player]['AST']), float(game_data[player]['STL']), float(game_data[player]['BLK'])]
                    big_matrix.append(vector)
        return big_matrix

    if createDataMatrix():
        all_matrices.append(createDataMatrix())
    print(all_matrices)