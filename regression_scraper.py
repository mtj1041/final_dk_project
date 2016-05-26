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
import json

full_data = {}
sport_ids = []

# Loads data into an automatically generated dictionary for a given player #
# TODO: Make a list of playerids for each sport and load them all # 

def loadData(sport, playerid):
    r = requests.get('http://espn.go.com/' + sport + '/player/gamelog/_/id/' + str(playerid))
    soup = BeautifulSoup(r.text, "html5lib")
    table = soup.find("table", attrs={"class":"tablehead"})
    if not table: # No table = no stats
        return
    stats_headers = table.find("tr", attrs={"class":"colhead"})
    if not stats_headers: # "No stats to show"
        return
    name = soup.find("h1").get_text()
    print(name)
    full_data[name] = {}
    even_data = table.find_all("tr", attrs={"class":"evenrow"})
    odd_data = table.find_all("tr", attrs={"class":"oddrow"})
    data = even_data + odd_data
    dict_keys = [i.get_text() for i in stats_headers]
    for i in data:
        data_row = [filtered.get_text() for filtered in filter(lambda x : str(type(x)) == "<class 'bs4.element.Tag'>", i)]
        if len(data_row) == len(dict_keys):
            full_data[name][data_row[0]] = {}
            new_keys, new_data = dict_keys[1:], data_row[1:]
            for _ in range(len(new_keys)):
                full_data[name][data_row[0]][new_keys[_]] = new_data[_]

def generateTeamLinks(sport):
    base_url = 'http://espn.go.com/' + sport + '/teams'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, "html5lib")
    links = soup.find_all("a", href=True)
    sport_links = []
    for i in links:
        if i.get_text() == 'Roster':
            sport_links.append("http://espn.go.com" + i['href'])
    return sport_links
   
def generateTeamIDs(base_url):
    print(base_url)
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, "html5lib")
    table = soup.find("table", attrs={"class":"tablehead"})
    even_data = table.find_all("tr", attrs={"class":"evenrow"})
    odd_data = table.find_all("tr", attrs={"class":"oddrow"})
    data = even_data + odd_data
    for i in data:
        href_data = i.find_all("a", href=True)
        if href_data:
            player_id = int(href_data[0]['href'].split("/")[-2])
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

def loadDataFromJSON(sport):
    filename = sport + "_data.txt"
    with open(filename) as json_data:
        all_data = json.load(json_data)
    
    return all_data

# for MLB #

full_data = loadDataFromJSON('nba')
        
        
    
    
    
    