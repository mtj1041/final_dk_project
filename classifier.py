from sklearn import linear_model
import numpy as np
import csv
from random import randint


ranker_weights = []

def getTrainData():
	return []

def partitionData():
	return ([],[])


def trainNewCoeffs(data, actual_points):
	clf = linear_model.LinearRegression()
	clf.fit(data, actual_points)
	return np.array(clf.intercept_).append(clf.coef_)

def loadSavedCoeffs():
	global ranker_weights
	ranker_weights = np.empty()
	with open('ranker_weights.csv', 'rb') as rwfile:
		csv_str = next(csv.reader(rwfile))
		ranker_weights = np.array([int(i) for i in csv_str])

def saveCoeffs():
	rank_str = ''
	for i in ranker_weights:
		rank_str += str(i)
	rank_str = rank_str
	with open('ranker_weights.csv','wb') as rwfile:
		wrtr = csv.writer(rwfile)
		wrtr.writerow(rank_str)

