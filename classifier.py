from sklearn import linear_model
import numpy as np
import csv
from random import randint
import data_miner


ranker_weights = []

def kFoldCV(k, data, labels):
	average = 0
	j = len(data) / k
	for i in range(k):
		print 'on partition ' + str(i)
		train_data = np.concatenate((data[:j*i], data[j*(i+1):]))
		train_lbl = np.concatenate((labels[:j*i], labels[j*(i+1):]))
		val_data = data[j*i: j*(i+1)]
		val_lbl = labels[j*i: j*(i+1)]
		clf = linear_model.LinearRegression()
		clf.fit(train_data, train_lbl)
		score = clf.score(val_data, val_lbl)
		average += score
	return average / float(k)


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

def webDataTrain():
	data_miner.populatev1()
	trainNewCoeffs(data_miner.getXmatrix(), data_miner.getYvector())

def trainingRoutine():
	webDataTrain()
	print kFoldCV(122, data_miner.getXmatrix(), data_miner.getYvector())
	saveCoeffs()
