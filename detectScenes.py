import os
import numpy as np
import math
from scipy import spatial
#import BhattacharyyaDistance.bhatta_dist as bd
from dictances import bhattacharyya
import matplotlib as mp
import matplotlib.pyplot as plt
from collections import OrderedDict

def buildMatrix(frames):
	matrix = [[0 for x in range(len(frames))] for y in range(len(frames))] 
	for i in range(len(frames)):
		for j in range(len(frames)):
			matrix[i][j] = distanceMetric(frames[i],frames[j])# similarity = 1 - distance
			if(matrix[i][j] == float('nan')):
				print(str(i) + '_' + str(j))
	return matrix

def bhatta( hist1,  hist2):
    # calculate mean of hist1
    h1_ = np.average(hist1);
    # calculate mean of hist2
    h2_ = np.average(hist2);
    # calculate score
    score = 0;
    for i in range(len(hist1)):
        score += math.sqrt( hist1[i] * hist2[i] );

    # print h1_,h2_,score;
    #При сравнении плана с самим собой может получиться отрицательное число под корнем
    try:
    	score = math.sqrt( 1 - ( 1 / math.sqrt(h1_*h2_*len(hist1)*len(hist1)) ) * score );
    except ValueError as e:
    	score = 0
    return score;


def distanceMetric(vector1, vector2): #попробуй soft cosine measure
	distance = spatial.distance.cosine(vector1,vector2)#bhatta(vector1, vector2)
	return distance

def costFunction(distanceMatrix, scenesVector):#additive cost function
	cost = 0
	for i in range(1,len(scenesVector)):
		for j in range(scenesVector[i - 1] + 1, scenesVector[i]):
			for k in range(scenesVector[i - 1] + 1, scenesVector[i]):
				cost += distanceMatrix[j][k]
	return cost

def distanceRange(D, start, stop):
	result = 0
	for i in range(start, stop):
		result += D[stop][i] + D[i][stop]
	return result

def sumsTable(D, N):	
	E = [[0 for x in range(N)] for y in range(N)] 
	E[0][0] = 0
	for i in range(0, N):
		E[i][i] = 0
		for j in range(i + 1, N):
			E[i][j] = E[i][j-1] + distanceRange(D, i, j)
			E[j][i] = E[i][j]
	return E

def getCJ(E, n, k, N, C):
	result = 0
	argmin = N
	if k != 1 :
		result = C[n][k - 1]
		for i in range(n, N - 1):
			iterationValue = E[n - 1][i - 1] + C[i + 1][k - 1]
			if result > iterationValue :
				result = iterationValue
				argmin = i
	else:
		result = E[n - 1][N - 1]

	return result, argmin

def costTable(D, K, N):	
	C = [[0 for x in range(K + 1)] for y in range(N + 1)] 
	J = [[0 for x in range(K + 1)] for y in range(N + 1)] 
	E = sumsTable(D, N)	
	for i in range(1, K + 1):
		for j in range(1, N + 1):
			CJ = getCJ(E, j, i, N, C)
			C[j][i] = CJ[0]
			J[j][i] = CJ[1]
	return C, J

def getDivision(J, K):
	t = []
	t.append(0)
	for i in range(1,K + 1):
		t.append(J[t[i - 1] + 1][K - i + 1])
	return t



def basicSceneDetect(features, shots, K, N, fmatrix):
	distanceMatrix = buildMatrix(features)

	try:
		plt.pcolormesh(distanceMatrix, cmap='magma', snap=True)
		plt.savefig(fmatrix + 'matrix.png', bbox_inches='tight', dpi=200)
		plt.close()
	except Exception as e:
		print(e)

	tables = costTable(distanceMatrix, K, N)
	division = getDivision(tables[1], K)
	divisionByFrames = []
	for i in range(1, len(division)):
		divisionByFrames.append([shots[division[i - 1]][0], shots[division[i] - 1][1]])

	try:
		plt.pcolormesh(distanceMatrix, cmap='magma', snap=True)
		plt.savefig(fmatrix + 'matrix.png', bbox_inches='tight', dpi=200)
		plt.close()
	except Exception as e:
		print(e)
	return (divisionByFrames, division)













































































