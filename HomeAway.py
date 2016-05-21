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
    pnts = 0
    rebs = 0
    asst = 0
    block = 0
    stl = 0
    to = 0
    count = 0
    apnts = 0
    arebs = 0
    aasst = 0
    ablock = 0
    astl = 0
    ato = 0
    acount = 0
    for array in data:
        if array[1][:2] == 'vs':
            if int(array[3]) > 10: #If they played more than 10 minutes
                count += 1
                rebs += float(array[-7])
                asst += float(array[-6])
                block += float(array[-5])
                stl += float(array[-4])
                to += float(array[-3])
                pnts += float(array[-1])
                print array[-1]
        elif array[1][0]== '@':
            if int(array[3]) > 10: #If they played more than 10 minutes
                acount += 1
                arebs += float(array[-7])
                aasst += float(array[-6])
                ablock += float(array[-5])
                astl += float(array[-4])
                ato += float(array[-3])
                apnts += float(array[-1])
                print array[-1]

    print('------------HOME-------------')
    print("Average points at home: " + str(pnts/count))
    print("Average rebounds at home: " + str(rebs/count))
    print("Average assists at home: " + str(asst/count))
    print("Average blocks at home: "  + str(block/count))
    print("Average steals at home: "  + str(stl/count))
    print("Average turnovers at home: " + str(to/count))
    print('------------AWAY-------------')
    print("Average points away: " + str(apnts/acount))
    print("Average rebounds away: " + str(arebs/acount))
    print("Average assists away: " + str(aasst/acount))
    print("Average blocks away: "  + str(ablock/acount))
    print("Average steals away: "  + str(astl/acount))
    print("Average turnovers away: " + str(ato/acount))
    

getStatsForMatchUp(3975)
