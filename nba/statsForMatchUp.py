import NBAstats



#Function that takes in a players ID (int) and the players opponent (String) as the abbreviation
#and returns that players average fantasy points against this opponent
def getStatsForMatchUp(playerID, OPP):
    if OPP == "GSW":
        OPP = "GS"
    return NBAstats.getStats(playerID, OPP)

    

getStatsForMatchUp(1966, 'TOR')
