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

#input: 
#String - defense of interest (i.e. Opponent of the player we are analyzing)...must be fully spelled out (i.e. "Los Angeles Lakers")
#String - position of our player (options: "PG, SG, SF, PF, C"...also "G" and "F" if you want)  
#output:
#dictionary of the stats that the defense gives up on average.
#i.e. {'PTS': '23.8', 'Season': '55.1', 'REB': '5.9', 'BLK': '0.4', 'TO': '3.2', 'Last 5': '61.4', '3PM': '2.3', 'Vs. Pos': 'PG', 'Team': 'Los Angeles Lakers', 'FT%': '80.7', 'AST': '8.6', 'STL': '1.8', 'Last 10': '58.0', 'FG%': '45.8'}
# 'Season', 'Last 5', and 'Last 10' are the average amount of fantasy points given up throughout the season, through the last 5 games, and the last 10 games, respectively
def getDefenseVsPosStats(defense, pos):
	url = 'http://www.rotowire.com/daily/nba/defense-vspos.htm?site=DraftKings'
	#PG has no extension, but the other positions do
	if pos != "PG":
		url = url + "&pos=" + pos
	r = requests.get(url)
	soup = BeautifulSoup(r.text)
	table = soup.find("table", attrs={"class":"tablesorter headerfollows footballproj-table"})
	statCategory = [t.get_text() for t in table.find_all('th')][3:] #array of stat categories such as 'REB', 'AST', etc. first 3 entries we don't want
	rows = table.find_all('tr') #all the rows in the table
	#Go through all of the rows and find the one that corresponds to the defense that we want to know about
	for r in rows:
		data = r.find_all('td')
		if len(data) > 0: 
			if data[0].get_text() == defense:
				break #once we find that defense, we break with 'data' as an array of bs4.tags corresponding to stats
	#go through that array of bs4.tags to just get the text. (i.e. <td>5.9</td> becomes 5.9)
	for i in range(len(data)):
		data[i] = data[i].get_text()

	#Create the array of defensive statistics that we are going to return
	defensiveStats = {}
	#Loop through the stats category we created earlier and point the category to the actual number (i.e. {"REB" -> 5.9})
	for i in range(len(statCategory)):
		defensiveStats[statCategory[i]] = data[i]

	return defensiveStats
	