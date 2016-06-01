import bs4
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
import re
import json

full_data = {}
sport_ids = []
other_changes = {"kike hernandez":"enrique hernandez", "b.j. upton":"melvin upton jr.", "j. saltalamacchia":"jarrod saltalamacchia", "c. bethancourt":"christian bethancourt"}

date_dict = {"Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11}
# Loads data into an automatically generated dictionary for a given player #
# TODO: Make a list of playerids for each sport and load them all # 

def loadData(sport, playerid):
    r = requests.get('http://espn.go.com/' + sport + '/player/_/id/' + str(playerid))
    soup = BeautifulSoup(r.text)

    pos = soup.find("li", attrs={"class":"first"})
    full = pos.get_text().split(" ")[-1]

    r = requests.get('http://espn.go.com/' + sport + '/player/gamelog/_/id/' + str(playerid))
    soup = BeautifulSoup(r.text)
    table = soup.find("table", attrs={"class":"tablehead"})
    if not table: # No table = no stats
        return
    stats_headers = table.find("tr", attrs={"class":"colhead"})
    if not stats_headers: # "No stats to show"
        return
    name = soup.find("h1").get_text().lower()
    print(name + " " + full)
    full_data[name] = {}
    full_data[name]['POS'] = full
    even_data = table.find_all("tr", attrs={"class":"evenrow"})
    odd_data = table.find_all("tr", attrs={"class":"oddrow"})
    data = even_data + odd_data
    dict_keys = [i.get_text() for i in stats_headers]
    for i in data:
        data_row = [filtered.get_text() for filtered in filter(lambda x : str(type(x)) == "<class 'bs4.element.Tag'>", i)]
        if len(data_row) == len(dict_keys):
            numeric_month = str(date_dict[data_row[0].split(" ")[0]])
            numeric_day = str(data_row[0].split(" ")[1]) if int(data_row[0].split(" ")[1]) > 9 else '0' + data_row[0].split(" ")[1]
            numeric_date = int(numeric_month + numeric_day)
            full_data[name][numeric_date] = {}
            new_keys, new_data = dict_keys[1:], data_row[1:]
            for _ in range(len(new_keys)):
                full_data[name][numeric_date][new_keys[_]] = new_data[_]


def loadDKPlayerData():
    positionDict = {'pg':'point-guards', 'sg' : 'shooting-guards', 'sf': 'small-forwards', 'pf' : 'power-forwards', 'c':'centers'}
    url = "http://www.rotowire.com/daily/mlb/optimizer.htm?site=DraftKings"
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    table = soup.find("tbody", attrs={"id":"players"})
    rows = table.find_all("tr")
    full_data['julio urias'] = {}
    for r in rows:
        data = r.find('td', attrs = {"class": "rwo-name align-l p10l"})
        name = (data.get_text().lower())
        spacer = '\xa0'
        name = name.split(spacer)[0] #Sometimes there are comments on a player (i.e. GTD for game time decision, how can we get rid of these?)
        if not name in full_data.keys():
            for i in full_data.keys():
                if name.split(" ")[0].split("-")[0] in i and name.split(" ")[-1] in i:
                    name = i
            if name in other_changes.keys():
                name = other_changes[name]
        posData = r.find('td', attrs = {"class": "rwo-pos align-c"}) 
        salaryData = r.find('td', attrs={"class":"rwo-salary basic"})

        pos = (posData.get_text().lower())
        print("NAME: " + name + " " + pos + " SALARY: " + salaryData.get_text()[1:].split(",")[0] + salaryData.get_text()[1:].split(",")[1])
        # Override, for the players that play today #
        full_data[name]['POS'] = pos
        full_data[name]['SALARY'] = salaryData.get_text()[1:].split(",")[0] + salaryData.get_text()[1:].split(",")[1]

def generateTeamLinks(sport):
    base_url = 'http://espn.go.com/' + sport + '/teams'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text)
    links = soup.find_all("a", href=True)
    sport_links = []
    for i in links:
        if i.get_text() == 'Roster':
            sport_links.append("http://espn.go.com" + i['href'])
    return sport_links
   
def generateTeamIDs(base_url):
    print(base_url)
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text)
    table = soup.find("table", attrs={"class":"tablehead"})
    even_data = table.find_all("tr", attrs={"class":"evenrow"})
    odd_data = table.find_all("tr", attrs={"class":"oddrow"})
    data = even_data + odd_data
    for i in data:
        href_data = i.find_all("a", href=True)
        if href_data:
            player_id = int(href_data[0]['href'].split("/")[-2])
            print(player_id)
            sport_ids.append(player_id)
    
def generateIDsForSports():
    links = generateTeamLinks('mlb')
    for link in links:
        generateTeamIDs(link)
        
# Loads data for all sports. Tested MLB/NBA, should work for all sports #
def loadPlayerDataForEntireSport(sport):
    links = generateTeamLinks(sport)
    for link in links:
        generateTeamIDs(link)
    for i in sport_ids:
        loadData(sport, i)
    filename = sport + '_data.txt'
    with open(filename, 'w') as outfile:
        json.dump(full_data, outfile)

# Loads pre-loaded JSON data #
# TODO: Each day, write new data into new JSON object. Or update weekly #
def loadDataFromJSON(sport):
    filename = sport + "_data.txt"
    with open(filename) as json_data:
        all_data = json.load(json_data)
    return all_data

def getTodaysMatchups(): # Just a test
    r = requests.get('http://dailybaseballdata.com/cgi-bin/dailyhit.pl?date=527&game=d&xyear=0&pa=0&showdfs=&sort=ops&r40=0&scsv=0')
    soup = BeautifulSoup(r.text)
    a_elems = soup.find_all("a")
    
    matchups = []        
    for i in range(len(a_elems)):
        if 'name' in a_elems[i].attrs:
            if not a_elems[i]['name'] == 'gameLast' and 'game' in a_elems[i]['name']:
                matchups.append((a_elems[i+1]['name'], a_elems[i+2]['name']))
    
    print(matchups)

def getMatchups(): # Real Function, ugly code, will fix later
    curr = datetime.datetime.now()
    year = str(curr.year)
    month = str(curr.month) if curr.month > 9 else ('0' + str(curr.month))
    day = str(curr.day) if curr.day > 9 else ('0' + str(curr.day))

    today = year + month + day

    r = requests.get('http://scores.espn.go.com/mlb/scoreboard/_/date/' + today)
    soup = BeautifulSoup(r.text)
    scripts = soup.find_all("script")
    
    matchups = []        
    for i in scripts:
        if '.scoreboardData' in i.get_text():
            m = i.get_text().split("window")[1].split("= ")[1].split(",")
            filtered, matchups = [], []
            for _ in m:
                if 'href' in _ and 'stats/batting/_/name/' in _:
                    filtered.append('http:' + _.split(":")[-1].split('"')[0])
            for x in range(len(filtered)):
                if x % 2 == 0:
                    matchups.append((filtered[x], filtered[x+1]))
    return matchups

def getTodaysPlayers():
    urls = getMatchups()

def getTodaysPitchers():
    curr = datetime.datetime.now()
    year = str(curr.year)
    month = str(curr.month) if curr.month > 9 else ('0' + str(curr.month))
    day = str(curr.day) if curr.day > 9 else ('0' + str(curr.day))

    today = year + "/" + month + "/" + day

    r = requests.get('http://mlb.mlb.com/news/probable_pitchers/?c_id=mlb&date=' + today)

    soup = BeautifulSoup(r.text)
    scripts = soup.find_all("a", href=True)

    pitchers = []
    forbidden_text = ['Career stats', 'Players of the week', 'Players of the month']
    for i in scripts:
        if 'player.jsp?player' in i['href'] and i.get_text() not in forbidden_text:
            pitchers.append(i.get_text().lower())

    new = list(set(pitchers))
    new.remove('')
    return new


def loadScoreboardFromJSON():
    filename = "scoreboards.txt"
    with open(filename) as json_data:
        all_data = json.load(json_data)
    return all_data
    

def getMLBData():
    return loadDataFromJSON('mlb')

# Missing players for some reason #
loadData('mlb', 31015)