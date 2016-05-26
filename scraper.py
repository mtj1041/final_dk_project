from bs4 import BeautifulSoup
from datetime import date
from operator import itemgetter
import requests
import time
import sys
import datetime
import operator
import numpy as np
import csv
import statsForMatchUp
import NBAids
import HomeAway
import trainer
import lastFive
playerIDs = NBAids.getIDs() #create a dictionary {playeer name -> player ID}

composite_data = {} #all data for each player
# e.g. { ... 'dwyane wade': {'TOPG': '2.7', 'AP48M': '6.1', 'FTM-FTA': '3.6-4.6', 'FG%': '.469', 
#'3PM-3PA': '0.9-1.6', 'STL/TO': '0.29', 'RPG': '5.6', 'TOTAL': 'MIA', '\xa0': '14', 'TO': 
#'38', 'APG': '4.3', 'TRIDBL': '0', 'ADJ': '21.4', 'ST/TO': '0.29', 'MPG': '33.8', 
#'AST/TO': '1.58', 'BLKPG': '0.9', 'AST': '60', 'STP48M': '1.12', 'ST/PF': '0.50', '3P%': 
#'.522', 'TOP48': '3.9', 'BLK/PF': '0.59', 'FT%': '.781', 'PF': '22', 'PTS': '21.4', 
#'TEAM': 'MIA', 'DBLDBL': '1', 'STL': '11', 'RP48': '8.0', 'FGM-FGA': '8.5-18.1', 'DRPG': '4.8', 
#'BLKP48M': '1.32', 'OFF': '12', 'ORPG': '0.9', 'REB': '79', 'GP': '14', 'PPG': '21.4', 
#'DEF': '67', 'STPG': '0.8', 'BLK': '13'}, 'serge ibaka': {'TOPG': '0.4', 'AP48M': '0.7', 
#'FTM-FTA': '0.5-0.6', 'FG%': '.528', '3PM-3PA': '1.7-3.4', 'STL/TO': '2.40', 'RPG': '5.9', 
#'TOTAL': 'OKC', '\xa0': '13', 'TO': '5', 'APG': '0.5', 'TRIDBL': '0', 'ADJ': '11.0', 'ST/TO': 
#'2.40', 'MPG': '32.2', 'AST/TO': '1.20', 'BLKPG': '1.2', 'AST': '6', 'STP48M': '1.38', 'ST/PF'
#: '0.34', '3P%': '.500' ... ) ... }
positions = {}
missing = []
fantasy_rankings = []

base_url = 'http://espn.go.com/nba/statistics/player/_/stat/scoring-per-game/sort/avgPoints/qualified/false/position/'


####################
#### Loads ALL player data (can we just load necessary players to speed things up?)
#### All data goes into composite data which is a dictionary in the form {plyaer -> (stat, stat, stat, ...)}
#### See an example of composite data above
####################
def loadAllData():
    urls = ['http://espn.go.com/nba/statistics/player/_/stat/scoring-per-game/sort/avgPoints/qualified/false/count/',
            'http://espn.go.com/nba/statistics/player/_/stat/rebounds/sort/avgRebounds/qualified/false/count/',
            'http://espn.go.com/nba/statistics/player/_/stat/turnovers/sort/avgTurnovers/qualified/false/count/',
            'http://espn.go.com/nba/statistics/player/_/stat/steals/sort/avgSteals/qualified/false/count/',
            'http://espn.go.com/nba/statistics/player/_/stat/3-points/sort/threePointFieldGoalPct/qualified/false/count/',
            'http://espn.go.com/nba/statistics/player/_/stat/assists/sort/avgAssists/qualified/false/count/',
            'http://espn.go.com/nba/statistics/player/_/stat/blocks/sort/avgBlocks/qualified/false/count/',
            'http://espn.go.com/nba/statistics/player/_/stat/double-doubles/sort/doubleDouble/qualified/false/count/',
            'http://espn.go.com/nba/statistics/player/_/stat/double-doubles/sort/tripleDouble/qualified/false/count/']

    for url in urls:
        loadPlayers = 1
        while loadPlayers < 452:
            split = url.split("/")
            split[-1] = str(loadPlayers)
            data = ""
            for i in split:
                data += i
                data += "/"
            print(data)
            #data is a url... the above procedure simply navigates to the appropriate page
            r = requests.get(data)
            soup = BeautifulSoup(r.text)
            table = soup.find("table", attrs={"class":"tablehead"}) #Go to the table with all of the stats
            if table.find("tr") == None:
                break 
            current_team = ''
            rows = [t.get_text() for t in table.find("tr")] 
            index = 0
            for i in table.find_all("td"):
                if i.get_text() not in rows:
                    if index % len(rows) > 0:
                        if index % len(rows) == 1:
                            team = i.get_text().split(",")[0]
                            # if url == 'http://espn.go.com/nba/statistics/player/_/stat/scoring-per-game/sort/avgPoints/qualified/false/count/':
                            #     loadID(team, data)
                            if team[-1] == '*':
                                team = team[:-1]
                            if len(team.lower().split(" ")) == 3:
                                split = team.lower().split(" ")
                                team = split[0] + " " + split[2]
                            if team.lower() not in composite_data.keys():
                                composite_data[team.lower()] = {}
                        else:
                            composite_data[team.lower()][rows[index % len(rows)]] = i.get_text()
                index += 1
            loadPlayers += 40 #Each page has 40 players so the next page will end in 41 then 81 etc.


#Finds the salaries of players playing today and puts in an ordered array called all_players_salary
#Order of this array will correspond to the order of all_players
# e.g. of all_players_salary: ['11100', '10300', '10700', '9500', '10500', '7900', '8300', '8400', 
#                              '8200', '7200', '6300', '5600', '6000', '4300', '4200', '5100', '4400', 
#                              '4800', '4100', '3900', '4500', '3800', '3100', '3300', '3200', '3000', 
#                              '2800', '3700', '2000', '2300', '2000', '2500', '2000', '2100', '2400', 
#                              '2000', '2000', '2000', '2000', '2000', '2000']
def loadSalaries():
    r = requests.get('http://www.rotowire.com/daily/nba/optimizer.htm?site=DraftKings')
    soup = BeautifulSoup(r.text)
    table = soup.find("table", attrs={"id":"playerPoolTable"})
    next_table2 = table.find_all("td", attrs={"class":"rwo-salary"})
    next_table = table.find_all("a")
    current_player = ''
    all_players = []
    all_players_salary = []
    missing_players = {"frank kaminsky":"frank iii", "joseph young":"joe young", "lou williams":"louis williams", "louis amundson":"lou amundson", "johnny o'bryant":"johnny iii", "luc moute":"luc richard mbah a moute", "j.j. hickson":"jj hickson", "cristiano fel\xc3\xadcio":"cristiano felicio", "roy marble":"devyn marble"}
    for i in next_table:
        name = i.get("title").lower() #used to be .encode(utf-8') but didnt work for me
        if name not in composite_data.keys():
            missing.append(name)
            if name in missing_players.keys():
                name = missing_players[name]
        if name in composite_data.keys():
            all_players.append(name)

    for i in next_table2:
        to_dollar = i.get_text()[1:].split(",")
        dollar_val = to_dollar[0] + "" + to_dollar[1]
        all_players_salary.append(dollar_val)

    for i in range(len(all_players)):
        composite_data[all_players[i]]['COST'] = all_players_salary[i]
    print("--------SALARIES---------")
    print(all_players_salary)


#Finds the games that are today (or if need be, can be customized as the commented out section foy May 22, 2016)
#returns a tuple of three items
# 1. todays games: array of strings in the format "TEAM1 vs. TEAM2" (teams are abbreviated)
# 2. todays teams: array of strings of all the teams playing e.g.: ["GSW", "CLE", "OKC" ... ]
# 3. dictionary of todays matchups going both ways. So if OKC was playing GSW then {GSW -> OKC, OKC -> GSW}
def loadMatchups():
    todays_games = []
    todays_teams = []
    todays_matchups = {}
    now = datetime.datetime.now()
    todays_date = ''
    todays_date += str(now.year)
    if now.month < 10:
        todays_date += '0'
    todays_date += str(now.month)
    if now.day < 10:
        todays_date += '0'
    todays_date += str(now.day)
    url = 'http://www.nba.com/gameline/'
    url += todays_date
    url += '/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    for link in soup.find_all('a'):
        first = link.get('href')
        if first:
            if "gameinfo.html" in first:
                teams = first[16:22]
                first_team = teams[0:3]
                second_team = teams[3:6]
                todays_teams.append(first_team)
                todays_teams.append(second_team)
                game_title = first_team + ' vs. ' + second_team
                todays_games.append(game_title)
                todays_matchups[first_team] = second_team
                todays_matchups[second_team] = first_team
    url = 'http://www.nba.com/gameline/20160527'
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    for link in soup.find_all('a'):
        first = link.get('href')
        if first:
            if "gameinfo.html" in first:
                teams = first[16:22]
                first_team = teams[0:3]
                second_team = teams[3:6]
                todays_teams.append(first_team)
                todays_teams.append(second_team)
                game_title = first_team + ' vs. ' + second_team
                todays_games.append(game_title)
                todays_matchups[first_team] = second_team
                todays_matchups[second_team] = first_team

    return (todays_games, todays_teams, todays_matchups)

#THIS FUNCTION MAY NEED SOME WORK- SOURCE SHOULD BE CHANGED SINCE THE POSITIONS DID NOT WORK ON DRAFT KINGS! IM THINKING ROTOWIRE?
#Function that adds a "POS" key to the composite_data dictionary with appropriate position (in the full spelled out way as in pos_list below)
# def loadPlayerPositions():
#     pos_list = ['point-guards', 'shooting-guards', 'small-forwards', 'power-forwards', 'centers']
#     for pos in pos_list:
#         base_url = 'http://espn.go.com/nba/statistics/player/_/stat/scoring-per-game/sort/avgPoints/qualified/false/position/' + pos + '/count/'
#         loadPlayers = 1
#         while loadPlayers < 452:
#             split = base_url.split("/")
#             split[-1] = str(loadPlayers)
#             data = ""
#             for i in split:
#                 data += i
#                 data += "/"
#             print(data)
#             r = requests.get(data)
#             soup = BeautifulSoup(r.text)
#             table = soup.find("table", attrs={"class":"tablehead"})
#             current_team = ''
#             rows = []
#             tr_elem = table.find("tr")
#             if tr_elem:
#                 for i in tr_elem:
#                     rows += i.get_text()
#             index = 0
#             for i in table.find_all("td", attrs={"align":"left"}):
#                 name = i.get_text()
#                 if ', ' in name:
#                     team = i.get_text().split(",")[0]
#                     if team[-1] == '*':
#                         team = team[:-1]
#                     if len(team.lower().split(" ")) == 3:
#                         split = team.lower().split(" ")
#                         team = split[0] + " " + split[2]
#                     composite_data[team.lower()]['POS'] = pos
#                     print(team.lower())
#             loadPlayers += 40

#Fixed
def loadPlayerPositions():
    positionDict = {'pg':'point-guards', 'sg' : 'shooting-guards', 'sf': 'small-forwards', 'pf' : 'power-forwards', 'c':'centers'}
    url = "http://www.rotowire.com/daily/nba/optimizer.htm?site=DraftKings"
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    table = soup.find("tbody", attrs={"id":"players"})
    rows = table.find_all("tr")
    for r in rows:
        data = r.find('td', attrs = {"class": "rwo-name align-l p10l"})
        name = (data.get_text().lower())
        spacer = u' \xa0'
        name = name.split(spacer, 1)[0] #Sometimes there are comments on a player (i.e. GTD for game time decision, how can we get rid of these?)
        posData = r.find('td', attrs = {"class": "rwo-pos align-c"}) 
        pos = (positionDict[posData.get_text().lower()])
        composite_data[name]['POS'] = pos


#Given the input of a team's url
#Returns and array of arrays that have lowercase names of each player
def loadRoster(team):
    rank_array = []
    url = team
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    for link in soup.find_all('a'):
        first = link.get('href')
        if 'http://espn.go.com/nba/player/_/id/' in first:
            team_list = first.split('/')
            beforeName = team_list[-1]
            name = beforeName.split("-")
            rank_array += [name[0] + " " + name[1]]
    return rank_array

#Dictionary {full team name -> abbreviation}
def makeDictionary():
    teamsDict = {}
    teams = ['san-antonio-spurs', 'cleveland-cavaliers', 'miami-heat', 'toronto-raptors', 'utah-jazz', 'memphis-grizzlies', 'orlando-magic', 'indiana-pacers', 'detroit-pistons', 'oklahoma-city-thunder', 'atlanta-hawks', 'new-york-knicks', 'boston-celtics', 'dallas-mavericks', 'charlotte-hornets', 'los-angeles-clippers', 'chicago-bulls', 'golden-state-warriors', 'milwaukee-bucks', 'portland-trail-blazers', 'minnesota-timberwolves', 'brooklyn-nets', 'denver-nuggets', 'washington-wizards', 'philadelphia-76ers', 'new-orleans-pelicans', 'houston-rockets', 'los-angeles-lakers', 'phoenix-suns', 'sacramento-kings']
    abbreviations = ['SAS', 'CLE', 'MIA', 'TOR', 'UTA', 'MEM', 'ORL', 'IND', 'DET', 'OKC', 'ATL', 'NYK', 'BOS', 'DAL', 'CHA', 'LAC', 'CHI', 'GSW', 'MIL', 'POR', 'MIN', 'BKN', 'DEN', 'WAS', 'PHI', 'NOP', 'HOU', 'LAL', 'PHX', 'SAC']
    for i in range(len(teams)):
        teamsDict[teams[i]] = abbreviations[i]
    return teamsDict

#Dictionary {abbreviation -> full team name}
def makeReverseDictionary():
    teamsDict = {}
    teams = ['san-antonio-spurs', 'cleveland-cavaliers', 'miami-heat', 'toronto-raptors', 'utah-jazz', 'memphis-grizzlies', 'orlando-magic', 'indiana-pacers', 'detroit-pistons', 'oklahoma-city-thunder', 'atlanta-hawks', 'new-york-knicks', 'boston-celtics', 'dallas-mavericks', 'charlotte-hornets', 'los-angeles-clippers', 'chicago-bulls', 'golden-state-warriors', 'milwaukee-bucks', 'portland-trail-blazers', 'minnesota-timberwolves', 'brooklyn-nets', 'denver-nuggets', 'washington-wizards', 'philadelphia-76ers', 'new-orleans-pelicans', 'houston-rockets', 'los-angeles-lakers', 'phoenix-suns', 'sacramento-kings']
    abbreviations = ['SAS', 'CLE', 'MIA', 'TOR', 'UTA', 'MEM', 'ORL', 'IND', 'DET', 'OKC', 'ATL', 'NYK', 'BOS', 'DAL', 'CHA', 'LAC', 'CHI', 'GSW', 'MIL', 'POR', 'MIN', 'BKN', 'DEN', 'WAS', 'PHI', 'NOP', 'HOU', 'LAL', 'PHX', 'SAC']
    for i in range(len(teams)):
        teamsDict[abbreviations[i]] = teams[i]
    return teamsDict

#Gets all of the players that are playing today by looking at the teams that are playing today (loadMatchups()[1])
#and loading the rosters for each of those teams (loadRoster)
#will then return a tuple of 2 elements
#1. array of all the players active today
#2. dictionary of {player -> his team (abbreviated)} (may not be needed because this data is already captured in the composite data dictionary)
def loadActiveRosters():
    players_playing = []
    playersTeam = {}
    todaysTeams = loadMatchups()[1]
    peoplePlaying = makeDictionary()
    url = 'http://espn.go.com/nba/teams'
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    for link in soup.find_all('a'):
        first = link.get('href')
        if 'http://espn.go.com/nba/team/_/name/' in first:
            new_name = first.split("/")
            appen = new_name[-2] + "/" + new_name[-1]
            new_url = 'http://espn.go.com/nba/team/roster/_/name/' + appen
            if peoplePlaying[new_name[len(new_name)-1]] in todaysTeams:
                print("Loading roster of " + peoplePlaying[new_name[len(new_name)-1]] + "...")
                playersOnTeam = loadRoster(new_url)
                players_playing += playersOnTeam
                for player in playersOnTeam:
                    playersTeam[player] = peoplePlaying[new_name[len(new_name)-1]]
    return (players_playing, playersTeam)

# loadID is not currently used... since we have the excel file with all of the IDs will need to be updated yearly though.
# the call to the function is in loadAllData but is commented out
def loadID(player, page):
    # url = 'http://espn.go.com/nba/statistics/player/_/stat/scoring-per-game/sort/avgPoints/qualified/false/'
    print(player)
    r = requests.get(page)
    soup = BeautifulSoup(r.text)
    lotsOfURLs = []
    for a in soup.find_all('a', href=True):
        urlString = a['href']
        urlArray = urlString.split('/')
        lotsOfURLs.append(urlArray)

    playerArray = player.lower().split(' ')
    for url in lotsOfURLs:
        playerString = playerArray[0] + "-" + playerArray[1]
        if playerString in url:
            playerIDs[playerString] = url[-2]

#Given the players that are playing today (array of names)
#will calculate the proj fantasy score and print the rankings for today
# returns an array of tuples that have (players proj points, player name)
def createFantasyRankings(players):
    print("PLAYERS")
    print(players)
    fantasy_data = []
    stats = ['PTS', 'REB', 'APG', 'STPG', 'BLKPG']
    for player in players:
        if player in composite_data.keys():
            three_points = composite_data[player]['3PM-3PA']
            # data format 3PM MADE PER GAME - 3PM ATTEMPTED PER GAME
            gp = float(composite_data[player]['GP'])
            pts = 0.5 * float(three_points.split("-")[0])
            pts += 1.5 * (float(composite_data[player]['DBLDBL']) / gp) + 3 * (float(composite_data[player]['TRIDBL']) / gp)
            pts += float(composite_data[player]['PTS']) + 1.25 * (float(composite_data[player]['REB']) / gp) + 1.5 * float(composite_data[player]['APG']) + 2 * float(composite_data[player]['STPG']) + 2 * float(composite_data[player]['BLKPG'])
            pts -= 0.5 * float(composite_data[player]['TOPG'])

            #calculate average fantasy points against opponent they are playing

            #######These next two lines are bad...need to fix
            players_own_team = composite_data[player]['TEAM']
            matchups = loadMatchups()[2]
            ############

            if player in playerIDs:
                playerID = playerIDs[player]
            else:
                continue
            playerTeam = players_own_team
            if playerTeam == "GS":
                playerTeam = "GSW"
            playerOpp = matchups[playerTeam]
            location = 'away'
            if playerTeam == 'GSW' or playerTeam == 'TOR':
                location = 'home'
            print(playerID)
            print(playerOpp)
            pntsAgainstOpp = statsForMatchUp.getStatsForMatchUp(playerID, playerOpp)
            homeAwayPts = HomeAway.getStatsForHomeAway(playerID, location)
            last5games = lastFive.getLastFive(player)
            #average overall points and points against opp
            w1, w2, w3, w4 = trainer.getWeights(player)
            avgPnts = (pts * w1) + (pntsAgainstOpp * w2) + (homeAwayPts * w3) + (last5games * w4)
            fantasy_data.append((avgPnts, player))
    print("fantasy DATA")
    print(fantasy_data)
    return fantasy_data



#######################
# function that will ultimately return a dictionary of {position -> array of player stats}
# where each element in the array of player stats consists of a tuple of ('name', price, projected_score)
# ex. results = {'point-guards': [('russell westbrook', 11100, 52), ('stephen curry', 10700, 47), ('kyle lowry', 8300, 37), 
#               ('kyrie irving', 8400, 37), ('shaun livingston', 3200, 19), ('cory joseph', 3100, 16), 
#               ('matthew dellavedova', 2400, 14)], 'forwards': [], 'small-forwards': [('kevin durant', 10300, 49), 
#               ('lebron james', 10500, 48), ('harrison barnes', 4300, 20), ('andre iguodala', 4200, 20), ... }
#######################
def todaysList():
    todays_players, players_own_team = loadActiveRosters()
    abbr_to_name = makeReverseDictionary()
    matchups = loadMatchups()[2]
    print("Loading all player data...")
    loadAllData()
    print("Loading salary data...")
    loadSalaries()
    print("Creating fantasy rankings...")
    loadPlayerPositions()
    fantasy_rankings = createFantasyRankings(todays_players)
    fantasy_rankings = sorted(fantasy_rankings, key=lambda x: x[0])[::-1]
    print("Today's fantasy rankings...")
    rank = 1
    for pos in ['point-guards', 'shooting-guards', 'small-forwards', 'power-forwards', 'centers', 'guards', 'forwards', 'util']:
        positions[pos] = []
    for i in fantasy_rankings:
        if 'COST' in composite_data[i[1]].keys():
            if (float(composite_data[i[1]]['COST'])) > 0 and (i[0] > 0):
                print(str(rank) + ". " + i[1] + ", Projected FPTS: " + str(i[0]) + " Cost: " + composite_data[i[1]]['COST'])
                positions[composite_data[i[1]]['POS']].append(i[1])
                positions['util']
                composite_data[i[1]]['FPTS'] = i[0]
                rank += 1
    result = {}
    for pos in positions:
        lst = positions[pos]
        tup_lst = [(name, int(composite_data[name]['COST']), float(composite_data[name]['FPTS'])) for name in lst]
        result[pos] = tup_lst
    return result