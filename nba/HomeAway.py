import NBAstats


def getStatsForHomeAway(playerID, location):
    return NBAstats.getStats(playerID, location)

    

getStatsForHomeAway(3449, 'away ')
