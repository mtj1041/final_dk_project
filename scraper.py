from bs4 import BeautifulSoup
from datetime import date
from operator import itemgetter
import requests
import time
import sys
import datetime
import operator

composite_data = {}
positions = {}
missing = []
fantasy_rankings = []

base_url = 'http://espn.go.com/nba/statistics/player/_/stat/scoring-per-game/sort/avgPoints/qualified/false/position/'

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
            r = requests.get(data)
            soup = BeautifulSoup(r.text)
            table = soup.find("table", attrs={"class":"tablehead"})
            current_team = ''
            rows = [t.get_text() for t in table.find("tr")]
            index = 0
            for i in table.find_all("td"):
                if i.get_text() not in rows:
                    if index % len(rows) > 0:
                        if index % len(rows) == 1:
                            team = i.get_text().split(",")[0]
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
            loadPlayers += 40


def loadSalaries():
    r = requests.get('http://www.rotowire.com/daily/nba/optimizer.htm?site=DraftKings')
    soup = BeautifulSoup(r.text)
    table = soup.find("table", attrs={"id":"playerPoolTable"})
    next_table2 = table.find_all("td", attrs={"class":"rwo-salary"})
    next_table = table.find_all("a")
    current_player = ''
    all_players = []
    all_players_salary = []
    missing_players = {"frank kaminsky":"frank iii", "joseph young":"joe young", "lou williams":"louis williams", "louis amundson":"lou amundson", "johnny o'bryant":"johnny iii", "luc moute":"luc richard mbah a moute", "j.j. hickson":"jj hickson", "cristiano felício":"cristiano felicio", "roy marble":"devyn marble"}
    for i in next_table:
        name = i.get("title").lower()
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


def loadMatchups():
    todays_games = []
    todays_teams = []
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
    return (todays_games, todays_teams)

def loadPlayerPositions():
    pos_list = ['point-guards', 'shooting-guards', 'small-forwards', 'power-forwards', 'centers']
    for pos in pos_list:
        base_url = 'http://espn.go.com/nba/statistics/player/_/stat/scoring-per-game/sort/avgPoints/qualified/false/position/' + pos + '/count/'
        loadPlayers = 1
        while loadPlayers < 452:
            split = base_url.split("/")
            split[-1] = str(loadPlayers)
            data = ""
            for i in split:
                data += i
                data += "/"
            print(data)
            r = requests.get(data)
            soup = BeautifulSoup(r.text)
            table = soup.find("table", attrs={"class":"tablehead"})
            current_team = ''
            rows = []
            tr_elem = table.find("tr")
            if tr_elem:
                for i in tr_elem:
                    rows += i.get_text()
            index = 0
            for i in table.find_all("td", attrs={"align":"left"}):
                name = i.get_text()
                if ', ' in name:
                    team = i.get_text().split(",")[0]
                    if team[-1] == '*':
                        team = team[:-1]
                    if len(team.lower().split(" ")) == 3:
                        split = team.lower().split(" ")
                        team = split[0] + " " + split[2]
                    composite_data[team.lower()]['POS'] = pos
            loadPlayers += 40


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

def makeDictionary():
    teamsDict = {}
    teams = ['san-antonio-spurs', 'cleveland-cavaliers', 'miami-heat', 'toronto-raptors', 'utah-jazz', 'memphis-grizzlies', 'orlando-magic', 'indiana-pacers', 'detroit-pistons', 'oklahoma-city-thunder', 'atlanta-hawks', 'new-york-knicks', 'boston-celtics', 'dallas-mavericks', 'charlotte-hornets', 'los-angeles-clippers', 'chicago-bulls', 'golden-state-warriors', 'milwaukee-bucks', 'portland-trail-blazers', 'minnesota-timberwolves', 'brooklyn-nets', 'denver-nuggets', 'washington-wizards', 'philadelphia-76ers', 'new-orleans-pelicans', 'houston-rockets', 'los-angeles-lakers', 'phoenix-suns', 'sacramento-kings']
    abbreviations = ['SAS', 'CLE', 'MIA', 'TOR', 'UTA', 'MEM', 'ORL', 'IND', 'DET', 'OKC', 'ATL', 'NYK', 'BOS', 'DAL', 'CHA', 'LAC', 'CHI', 'GSW', 'MIL', 'POR', 'MIN', 'BKN', 'DEN', 'WAS', 'PHI', 'NOP', 'HOU', 'LAL', 'PHX', 'SAC']
    for i in range(len(teams)):
        teamsDict[teams[i]] = abbreviations[i]
    return teamsDict

def makeReverseDictionary():
    teamsDict = {}
    teams = ['san-antonio-spurs', 'cleveland-cavaliers', 'miami-heat', 'toronto-raptors', 'utah-jazz', 'memphis-grizzlies', 'orlando-magic', 'indiana-pacers', 'detroit-pistons', 'oklahoma-city-thunder', 'atlanta-hawks', 'new-york-knicks', 'boston-celtics', 'dallas-mavericks', 'charlotte-hornets', 'los-angeles-clippers', 'chicago-bulls', 'golden-state-warriors', 'milwaukee-bucks', 'portland-trail-blazers', 'minnesota-timberwolves', 'brooklyn-nets', 'denver-nuggets', 'washington-wizards', 'philadelphia-76ers', 'new-orleans-pelicans', 'houston-rockets', 'los-angeles-lakers', 'phoenix-suns', 'sacramento-kings']
    abbreviations = ['SAS', 'CLE', 'MIA', 'TOR', 'UTA', 'MEM', 'ORL', 'IND', 'DET', 'OKC', 'ATL', 'NYK', 'BOS', 'DAL', 'CHA', 'LAC', 'CHI', 'GSW', 'MIL', 'POR', 'MIN', 'BKN', 'DEN', 'WAS', 'PHI', 'NOP', 'HOU', 'LAL', 'PHX', 'SAC']
    for i in range(len(teams)):
        teamsDict[abbreviations[i]] = teams[i]
    return teamsDict


def loadActiveRosters():
    players_playing = []
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
                players_playing += loadRoster(new_url)
    return players_playing

def createFantasyRankings(players):
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
            fantasy_data.append((pts, player))
    return fantasy_data


def todaysList():
    todays_players = loadActiveRosters()
    abbr_to_name = makeReverseDictionary()
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
    for pos in ['point-guards', 'shooting-guards', 'small-forwards', 'power-forwards', 'centers']:
        positions[pos] = []
    for i in fantasy_rankings:
        if 'COST' in composite_data[i[1]].keys():
            if (float(composite_data[i[1]]['COST'])) > 2000 and (i[0] > 20):
                print(str(rank) + ". " + i[1] + ", Projected FPTS: " + str(i[0]) + " Cost: " + composite_data[i[1]]['COST'])
                positions[composite_data[i[1]]['POS']].append(i[1])
                composite_data[i[1]]['FPTS'] = i[0]
                rank += 1

    result = {}
    for pos in positions:
        lst = positions[pos]
        tup_lst = [(name, int(composite_data[name]['COST']), int(composite_data[name]['FPTS'])) for name in lst)]
        result[pos] = tup_lst
    return result