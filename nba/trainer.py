import NBAids
import regression_scraper
import operator
import sys
import datetime
import numpy as np
import NBAstats
from collections import deque

A_matrix = None

def getWeights(player):
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

	opponentScores = {'MIL': 0, 'GS': 0, 'MIN': 0, 'MIA': 0, 'ATL': 0, 'BOS': 0, 'DET': 0, 'NY': 0, 'DEN': 0, 'DAL': 0, 'BKN': 0, 'POR': 0, 'ORL': 0, 'TOR': 0, 'CHI': 0, 'SA': 0, 'CHA': 0, 'UTAH': 0, 'CLE': 0, 'HOU': 0, 'WSH': 0, 'LAL': 0, 'PHI': 0, 'MEM': 0, 'LAC': 0, 'SAC': 0, 'OKC': 0, 'PHX': 0, 'IND': 0, 'NO': 0}
	homeAwayScores = {'home': 0, 'away': 0}
	opponentScoresCount = {'MIL': 0, 'GS': 0, 'MIN': 0, 'MIA': 0, 'ATL': 0, 'BOS': 0, 'DET': 0, 'NY': 0, 'DEN': 0, 'DAL': 0, 'BKN': 0, 'POR': 0, 'ORL': 0, 'TOR': 0, 'CHI': 0, 'SA': 0, 'CHA': 0, 'UTAH': 0, 'CLE': 0, 'HOU': 0, 'WSH': 0, 'LAL': 0, 'PHI': 0, 'MEM': 0, 'LAC': 0, 'SAC': 0, 'OKC': 0, 'PHX': 0, 'IND': 0, 'NO': 0}
	homeAwayScoresCount = {'home': 0, 'away': 0}
	actualPoints = []
	rollingAverage = []
	homeAway = []
	againstSpecificOpponent = []
	last5games = []
	last5q = deque(maxlen = 5)
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
	for game in sorted_Stats:
		gameCount += 1
		stats = game[1]
		homeAwayOpponent = stats['OPP']
		location = 'home'
		if "@" in homeAwayOpponent:
			location = 'away'
		opponent = homeAwayOpponent[2:]
		if u'\xa0' in opponent:
			continue
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
		

		fantasyPoints = NBAstats.getFantasyPoints(pnts, rebs, assts, blocks, steals, to, threes, tpldbl, dbldbl, 1)
		last5q.append(fantasyPoints)
		opponentScores[opponent] += fantasyPoints
		opponentScoresCount[opponent] += 1
		homeAwayScores[location] += fantasyPoints
		homeAwayScoresCount[location] += 1
		

		if gameCount > 10:
			total = 0
			print(last5q)
			for elem in last5q:
				total += elem
			last5games.append(total/5)
			totalFantasyPoints = NBAstats.getFantasyPoints(totalpnts, totalrebs, totalassts, totalblocks, totalsteals, totalto, totalthrees, totaltpldbl, totaldbldbl, gameCount)
			rollingAverage.append(totalFantasyPoints)
			actualPoints.append(fantasyPoints)
			homeAway.append(homeAwayScores[location]/homeAwayScoresCount[location])
			if opponentScoresCount != 0:
				againstSpecificOpponent.append(opponentScores[opponent]/opponentScoresCount[opponent])
			else:
				againstSpecificOpponent.append(totalFantasyPoints)

	y = np.transpose(np.matrix(actualPoints))
	#print(y)
	a1 = np.matrix(rollingAverage)
	a2 = np.matrix(againstSpecificOpponent)
	a3 = np.matrix(homeAway)
	a4 = np.matrix(last5games)
	A = np.transpose(np.vstack((a1,a2,a3, a4)))
	#print(A)
	x = np.linalg.lstsq(A, y)[0]
	return x

def getAMatrix(player):
	if player == 'james michael':
		return
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

	opponentScores = {'MIL': 0, 'GS': 0, 'MIN': 0, 'MIA': 0, 'ATL': 0, 'BOS': 0, 'DET': 0, 'NY': 0, 'DEN': 0, 'DAL': 0, 'BKN': 0, 'POR': 0, 'ORL': 0, 'TOR': 0, 'CHI': 0, 'SA': 0, 'CHA': 0, 'UTAH': 0, 'CLE': 0, 'HOU': 0, 'WSH': 0, 'LAL': 0, 'PHI': 0, 'MEM': 0, 'LAC': 0, 'SAC': 0, 'OKC': 0, 'PHX': 0, 'IND': 0, 'NO': 0}
	homeAwayScores = {'home': 0, 'away': 0}
	opponentScoresCount = {'MIL': 0, 'GS': 0, 'MIN': 0, 'MIA': 0, 'ATL': 0, 'BOS': 0, 'DET': 0, 'NY': 0, 'DEN': 0, 'DAL': 0, 'BKN': 0, 'POR': 0, 'ORL': 0, 'TOR': 0, 'CHI': 0, 'SA': 0, 'CHA': 0, 'UTAH': 0, 'CLE': 0, 'HOU': 0, 'WSH': 0, 'LAL': 0, 'PHI': 0, 'MEM': 0, 'LAC': 0, 'SAC': 0, 'OKC': 0, 'PHX': 0, 'IND': 0, 'NO': 0}
	homeAwayScoresCount = {'home': 0, 'away': 0}
	actualPoints = []
	rollingAverage = []
	homeAway = []
	againstSpecificOpponent = []
	last5games = []
	last5q = deque(maxlen = 5)
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
	for game in sorted_Stats:
		gameCount += 1
		stats = game[1]
		homeAwayOpponent = stats['OPP']
		location = 'home'
		if "@" in homeAwayOpponent:
			location = 'away'
		opponent = homeAwayOpponent[2:]
		if u'\xa0' in opponent:
			continue
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
		

		fantasyPoints = NBAstats.getFantasyPoints(pnts, rebs, assts, blocks, steals, to, threes, tpldbl, dbldbl, 1)
		last5q.append(fantasyPoints)
		opponentScores[opponent] += fantasyPoints
		opponentScoresCount[opponent] += 1
		homeAwayScores[location] += fantasyPoints
		homeAwayScoresCount[location] += 1
		

		if gameCount > 10:
			total = 0
			#print(last5q)
			for elem in last5q:
				total += elem
			last5games.append(total/5)
			totalFantasyPoints = NBAstats.getFantasyPoints(totalpnts, totalrebs, totalassts, totalblocks, totalsteals, totalto, totalthrees, totaltpldbl, totaldbldbl, gameCount)
			rollingAverage.append(totalFantasyPoints)
			actualPoints.append(fantasyPoints)
			homeAway.append(homeAwayScores[location]/homeAwayScoresCount[location])
			if opponentScoresCount != 0:
				againstSpecificOpponent.append(opponentScores[opponent]/opponentScoresCount[opponent])
			else:
				againstSpecificOpponent.append(totalFantasyPoints)

	y = np.transpose(np.matrix(actualPoints))
	#print(y)
	a1 = np.matrix(rollingAverage)
	a2 = np.matrix(againstSpecificOpponent)
	a3 = np.matrix(homeAway)
	a4 = np.matrix(last5games)
	A = np.transpose(np.vstack((a1,a2,a3, a4)))
	#print(A)
	return (A, y)

		
#getWeights('kevin love')
