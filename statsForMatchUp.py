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




#Function that takes in a players ID (int) and the players opponent (String) as the abbreviation
#and returns that players average fantasy points against this opponent
def getStatsForMatchUp(playerID, OPP):
    if OPP == "GSW":
        OPP = "GS"
    try: #I was running into an error that I couldn't figure out in which the line "if array[1][0]== '@' or array[1][:2] == 'vs':" 
         #said it was out of range... couldn't figure out why so for now I have this try, catch
        base_url = 'http://espn.go.com/nba/player/gamelog/_/id/'
        page = base_url + str(playerID)
        print(page)
        r = requests.get(page)
        #soup = BeautifulSoup(r.text, 'lxml')
        soup = BeautifulSoup(r.text)
        table = soup.find("table",{"class" : "tablehead"}) #this is the table with all of the statistics
        #data is an array of arrays... the inner arrays are all of the data points for each row
        data = [[stat.get_text() for stat in t.find_all("td")] for t in table.find_all("tr")]
        #We only want to keep the arrays that are 17 in length as that corresponds to the correct statistical elements
        for array in data: 
            if len(array) != 17:
                data.remove(array)
        #initialize this players statistcs against opponent as all zeros
        three = 0
        pnts = 0
        rebs = 0
        asst = 0
        block = 0
        stl = 0
        to = 0
        count = 0
        dbldbl = 0
        tpldbl = 0
        for array in data:
            if array[1][0]== '@' or array[1][:2] == 'vs': #this means that we have a correct row... this row has stats against a certain team
            #it doesn't really matter if they are home or away, it is just a way of ensuring that we are looking at the right kind of data
                #if we find that the row corresponds to a game against the opponent of interest
                if (array[1][2:]) == OPP:
                    if float(array[3]) > 10: #If they played more than 10 minutes
                        #add on to the data
                        count += 1.0
                        three = float(str(array[-11]).split("-")[0])
                        rebs += float(array[-7])
                        asst += float(array[-6])
                        block += float(array[-5])
                        stl += float(array[-4])
                        to += float(array[-2])
                        pnts += float(array[-1])
                        stat = [float(array[-1]),float(array[-4]),float(array[-5]),float(array[-6]),float(array[-7])]
                        countdouble = 0
                        #test for triple doubles and double doubles
                        for s in stat:
                            if s >= 10:
                                countdouble += 1.0
                        if countdouble == 2:
                            dbldbl += 1.0
                        elif countdouble > 2:
                            tpldbl += 1.0
        #if they never played, then we are going to return 0 to avoid 'divide by 0' error
        if count == 0:
            return 0
        #Find the averages 
        pnts = pnts/count
        three = three/count
        rebs = rebs/count
        asst = asst/count
        block = block/count
        stl = stl/count
        to = to/count
        dbldbl = dbldbl/count
        tpldbl = tpldbl/count
        print("Average points against " + OPP +": " + str(pnts))
        print("Average three pointers made against " + OPP +": " + str(three))
        print("Average rebounds against " + OPP +": " + str(rebs))
        print("Average assists against " + OPP +": " + str(asst))
        print("Average blocks against " + OPP +": " + str(block))
        print("Average steals against " + OPP +": " + str(stl))
        print("Average turnovers against " + OPP +": " + str(to))
        print("Likelihood of a double-double againts " + OPP + ": " + str(float(dbldbl)))
        print("Likelihood of a triple-double againts " + OPP + ": " + str(float(tpldbl)))
        #Calculate the total fantasy points
        fantasypnts = 0.5 * three
        fantasypnts += 1.5*dbldbl + 3*tpldbl
        fantasypnts += pnts + 1.25*rebs + 1.5*asst + 2*stl + 2*block
        fantasypnts -= 0.5*to
        fantasypnts = fantasypnts
        print("Average total fantasy points against " + OPP + ": " + str(fantasypnts))
        return fantasypnts
    except:
        return 0

    

#getStatsForMatchUp(1966, 'GS')
