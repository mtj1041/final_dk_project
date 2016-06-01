import regression_scraper
import json

#full_data = regression_scraper.getMLBData()
full_data = regression_scraper.getMLBData()

def determineAverageFPts(player):
    ab = 0 # games played where AB > 0
    hits = 0
    gp = 0
    tp = 0
    if full_data[player]['POS'] == 'SP' or full_data[player]['POS'] == 'RP':
        for i in full_data[player].keys():
            if not i == 'POS':
                gp += 1
                ip = float(full_data[player][i]['IP'])
                so = float(full_data[player][i]['SO'])
                w = 4 if full_data[player][i]['RESULT'][0] == 'W' else 0
                er = float(full_data[player][i]['ER'])
                h = float(full_data[player][i]['H'])
                bb = float(full_data[player][i]['BB'])
                cg = 2.5 if ip == 9.0 else 0
                cgso = 2.5 if ip == 9.0 and er == 0 else 0
                nh = 5 if h == 0 else 0
                pts = 2.25 * ip + 2 * so + w - 2 * er - 0.6 * h - 0.6 * bb + cg + cgso + nh
                full_data[player][i]['FPTS'] = pts
                tp += pts
    else:
        for i in full_data[player].keys():
            if not i == 'POS':
                gp += 1
                hits = int(full_data[player][i]['H'])
                doubles = int(full_data[player][i]['2B'])
                triples = int(full_data[player][i]['3B'])
                hr = int(full_data[player][i]['HR'])
                singles = hits - doubles - triples - hr
                runs = int(full_data[player][i]['R'])
                sb = int(full_data[player][i]['SB'])
                bb = int(full_data[player][i]['BB'])
                rbi = int(full_data[player][i]['RBI'])
                pts = (3 * singles) + 5 * doubles + 3 * triples + 10 * hr + 2 * rbi + 2 * bb + 5 * sb
                full_data[player][i]['FPTS'] = pts
                tp += pts
    return tp / gp

def regressionOverall(player): # Average points ON THE DAY OF BEING PLAYED. Prior to the results of that game.
    total_pts = 0
    gp = 0
    sorted_keys = sorted(full_data[player].keys())
    for i in range(len(sorted_keys)-1):
        if i == 0:
            gp = 1
        for x in range(0, i):
            gp += 1
            total_pts += full_data[player][sorted_keys[x]]['FPTS']
        full_data[player][sorted_keys[i]]['REG-OVERALL'] = total_pts / gp
        total_pts = 0
        gp = 0
    print("Loaded overall point averages for " + player)

# [1, 2, 3, 4, 5, 6, 7, 8] #
#  Index = 6
def lastFiveAverage(player):
    sorted_keys = sorted(full_data[player].keys()) # POS will always be the last key
    total_iterated = 0
    tp = 0
    for i in range(len(sorted_keys) - 1):
        if i == 0:
            total_iterated += 1
        elif i < 5 and i > 0:
            for x in range(0, i):
                total_iterated += 1
                tp += full_data[player][sorted_keys[x]]['FPTS']
        else:
            for x in range(i-5, i):
                total_iterated += 1
                tp += full_data[player][sorted_keys[x]]['FPTS']
        full_data[player][sorted_keys[i]]['REG-LAST-FIVE'] = tp / total_iterated
        tp = 0
        total_iterated = 0

def stadiumAverages(player):
    sorted_keys = sorted(full_data[player].keys())
    gp, tp = 0, 0
    home = False
    for i in range(len(sorted_keys) - 1):
        if i == 0:
            full_data[player][sorted_keys[i]]['REG-STADIUM-AVG'] = 0
        else:
            if (full_data[player]['POS'] == 'SP' or full_data[player]['POS'] == 'RP'):
                key = 'OPPONENT'
            else:
                key = 'OPP'
            stadium = full_data[player][sorted_keys[i]][key]
            if 'vs' in stadium:
                home = True
            for x in range(0, i):
                if stadium == full_data[player][sorted_keys[x]][key] or (home and 'vs' in full_data[player][sorted_keys[x]][key]):
                    gp += 1
                    tp += full_data[player][sorted_keys[x]]['FPTS']
            if not gp == 0:
                full_data[player][sorted_keys[i]]['REG-STADIUM-AVG'] = tp/gp
            else:
                full_data[player][sorted_keys[i]]['REG-STADIUM-AVG'] = 0
            tp = 0
            gp = 0
            home = False

def againstTeamAvg(player):
    sorted_keys = sorted(full_data[player].keys())
    gp, tp = 0, 0
    for i in range(len(sorted_keys) - 1):
        if i == 0:
            full_data[player][sorted_keys[i]]['REG-TEAM-AVG'] = 0
        else:
            if (full_data[player]['POS'] == 'SP' or full_data[player]['POS'] == 'RP'):
                key = 'OPPONENT'
            else:
                key = 'OPP'
            opponent = full_data[player][sorted_keys[i]][key].split(" ")[-1]

            for x in range(0, i):
                if opponent == full_data[player][sorted_keys[x]][key].split(" ")[-1]:
                    gp += 1
                    tp += full_data[player][sorted_keys[x]]['FPTS']
            if not gp == 0:
                full_data[player][sorted_keys[i]]['REG-TEAM-AVG'] = tp/gp
            else:
                full_data[player][sorted_keys[i]]['REG-TEAM-AVG'] = 0
            tp = 0
            gp = 0

def createAveragesForPlayer(player):
    print("Loading averages for player " + player + "...")
    regressionOverall(player)
    lastFiveAverage(player)
    stadiumAverages(player)
    againstTeamAvg(player)

def rankAllMLBPlayers(playerslist):
    players = []
    for i in playerslist:
        players.append((i, determineAverageFPts(i)))

    sorted_players = sorted(players, key=lambda x: x[1])[::-1]
    index = 1
    for i in sorted_players:
        print(str(index) + ". " + i[0] + " Average FPts: " + str(i[1]))
        index += 1

def writeAveragesToJSON():
    #regression_scraper.loadPlayerDataForEntireSport('mlb')
    for player in full_data.keys():
        if not (full_data[player]['POS'] == 'SP' or full_data[player]['POS'] == 'RP'):
            keys = list(full_data[player].keys())
            for i in keys:
                if not i == 'POS':
                    if full_data[player][i]['AB'] == '0':
                        del full_data[player][i]
    for i in full_data.keys():
        determineAverageFPts(i)
        createAveragesForPlayer(i)
    with open('mlb_data.txt', 'w') as outfile:
        json.dump(full_data, outfile)
    # write to JSON #