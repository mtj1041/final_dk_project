import NBAids
import regression_scraper
import operator
import sys
import datetime
import numpy as np
import NBAstats
from collections import deque
def getLastFive(player):

	fullList = regression_scraper.loadDataFromJSON('nba')
	playerSeasonStats = fullList[player]
	newSeasonStats = {}
	for dayAndDate in playerSeasonStats:
		date = dayAndDate.split(" ")[1]
		month = int(date.split('/')[0])
		day = int(date.split('/')[1])
		year = 2016
		if month > 8: 
			year = 2015
		actualDate = datetime.date(year, month, day)
		newSeasonStats[actualDate] = playerSeasonStats[dayAndDate]

	sorted_Stats = sorted(newSeasonStats.items(), key=operator.itemgetter(0))
	indices = [-1, -2, -3, -4, -5]
	fiveGames = []
	for i in indices:
		fiveGames.append(sorted_Stats[i])

	gameCount = 0
	totalpnts = 0
	totalrebs = 0
	totalassts = 0
	totalblocks = 0
	totalsteals = 0
	totalto = 0
	totalthrees = 0
	totaltpldbl = 0
	totaldbldbl = 0
	for game in fiveGames:
		stats = game[1]
		homeAwayOpponent = stats['OPP']
		opponent = homeAwayOpponent[2:]
		if u'\xa0' in opponent:
			continue

		gameCount += 1
		

		pnts = int(stats['PTS'])
		rebs = int(stats['REB'])
		assts = int(stats['AST'])
		blocks = int(stats['BLK'])
		steals = int(stats['STL'])
		to = int(stats['TO'])
		threes = int(stats['3PM-3PA'].split('-')[0])
		tpldbl = 0
		dbldbl = 0

		doubledoublecheck = [pnts, rebs, assts, blocks, steals]
		doubledoublecount = 0
		for s in doubledoublecheck:
			if s >= 10:
				doubledoublecount += 1.0
		if doubledoublecount == 2:
			dbldbl = 1.0
		elif doubledoublecount > 2:
			tpldbl = 1.0

		totalpnts += pnts
		totalrebs += rebs
		totalassts += assts
		totalblocks += blocks
		totalsteals += steals
		totalto += to
		totalthrees += threes
		totaltpldbl += tpldbl
		totaldbldbl += dbldbl

		return NBAstats.getFantasyPoints(totalpnts, totalrebs, totalassts, totalblocks, totalsteals, totalto, totalthrees, totaltpldbl, totaldbldbl, gameCount)