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
#import lxml


base_url = 'http://espn.go.com/nba/player/gamelog/_/id/'


def getStatsForMatchUp(playerID):
    page = base_url + str(playerID)
    print(page)
    r = requests.get(page)
    #soup = BeautifulSoup(r.text, 'lxml')
    soup = BeautifulSoup(r.text)
    table = soup.find("table",{"class" : "tablehead"})
    data = [[stat.get_text() for stat in t.find_all("td")] for t in table.find_all("tr")]
    for array in data: 
        if len(array) != 17:
            data.remove(array)

    Sun = 0
    Mon = 0
    Tue = 0
    Wed = 0
    Thu = 0
    Fri = 0
    Sat = 0
    Suncount = 0
    Moncount = 0
    Tuecount = 0
    Wedcount = 0
    Thucount = 0
    Fricount = 0
    Satcount = 0
    for array in data:
        if array[0][:3] == 'Sun':
            Sun += float(array[-1])
            Suncount += 1
        elif array[0][:3] == 'Mon':
            Mon += float(array[-1])
            Moncount += 1
        elif array[0][:3] == 'Tue':
            Tue += float(array[-1])
            Tuecount += 1
        elif array[0][:3] == 'Wed':
            Wed += float(array[-1])
            Wedcount += 1
        elif array[0][:3] == 'Thu':
            Thu += float(array[-1])
            Thucount += 1
        elif array[0][:3] == 'Fri':
            Fri += float(array[-1])
            Fricount += 1
        elif array[0][:3] == 'Sat':
            Sat += float(array[-1])
            Satcount += 1
    print(str(Sun/Suncount))
    print(str(Mon/Moncount))
    print(str(Tue/Tuecount))
    print(str(Wed/Wedcount))
    print(str(Thu/Thucount))
    print(str(Fri/Fricount))
    print(Sat/Satcount)

            


getStatsForMatchUp(25)
