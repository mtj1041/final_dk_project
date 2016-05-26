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

full_data = {}

# Loads data into an automatically generated dictionary for a given player #
# TODO: Make a list of playerids for each sport and load them all # 

def loadData(sport, playerid):
    r = requests.get('http://espn.go.com/' + sport + '/player/gamelog/_/id/' + str(playerid))
    soup = BeautifulSoup(r.text)
    table = soup.find("table", attrs={"class":"tablehead"})
    stats_headers = table.find("tr", attrs={"class":"colhead"})
    name = soup.find("h1").get_text()
    full_data[name] = {}
    even_data = table.find_all("tr", attrs={"class":"evenrow"})
    odd_data = table.find_all("tr", attrs={"class":"oddrow"})
    data = even_data + odd_data
    dict_keys = [i.get_text() for i in stats_headers]
    index = 0
    for i in data:
        data_row = [filtered.get_text() for filtered in filter(lambda x : str(type(x)) == "<class 'bs4.element.Tag'>", i)]
        if len(data_row) == len(dict_keys):
            full_data[name][data_row[0]] = {}
            new_keys, new_data = dict_keys[1:], data_row[1:]
            for _ in range(len(new_keys)):
                full_data[name][data_row[0]][new_keys[_]] = new_data[_]