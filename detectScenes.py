import os

os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
import keras
import cv2
import numpy as np
import math
from scipy import spatial



def readData():
	fs = open('data/1/shots.txt')
	fv = cv2.VideoCapture('data/1/video.mp4')
	shots = readShots(fs)
	return (shots, fv)

def readShots(shotFile):
	array = []
	for line in shotFile: # read rest of lines
		array.append([int(x) for x in line.split()])
	return array

def readImageFromVideo(video, index):
	totalFrames = video.get(cv2.CAP_PROP_FRAME_COUNT)
	if index > totalFrames or index < 0:
		print('Кадр за границами видео')
		return 0
	video.set(cv2.CAP_PROP_POS_FRAMES, index)
	ret, frame = video.read()
	img = cv2.resize(frame,(299,299))
	img = np.reshape(img,[1,299,299,3])

	return img

def buildMatrix(frames):
	matrix = [[0 for x in range(len(frames))] for y in range(len(frames))] 
	for i in range(len(frames)):
		for j in range(len(frames)):
			matrix[i][j] = distanceMetric(frames[i],frames[j])# similarity = 1 - distance

	return matrix

def distanceMetric(vector1, vector2): #попробуй soft cosine measure
	distance = spatial.distance.cosine(vector1,vector2)
	return distance

def costFunction(distanceMatrix, scenesVector):#additive cost function
	cost = 0
	for i in range(1,len(scenesVector)):
		for j in range(scenesVector[i - 1] + 1, scenesVector[i]):
			for k in range(scenesVector[i - 1] + 1, scenesVector[i]):
				cost = cost + distanceMatrix[j][k]
	return cost

def distanceRange(D, start, stop):
	result = 0
	for i in range(start, stop):
		result = result + D[stop][i] + D[i][stop]
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
	np.savetxt('E.txt', E, '%f')
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




data = readData()
model = keras.applications.xception.Xception(include_top=False, weights='imagenet', pooling='avg')

frame = model.predict(readImageFromVideo(data[1], 10))
#print(frame[0]) 2048 parameters

K = 70#0 #белое солнце
N = 720#len(predictedFrames)
predictedFrames = []
shotIndex = 0
for shot in data[0][0:N]:
	shotIndex = shotIndex + 1
	#print('predicting frame ' + str(shotIndex))
	imageIndex = (shot[0] + shot[1]) / 2
	image = readImageFromVideo(data[1], imageIndex)
	middleFrame = model.predict(image)
	predictedFrames.append(middleFrame[0])
distanceMatrix = buildMatrix(predictedFrames)
#print(distanceMatrix)


tables = costTable(distanceMatrix, K, N)

division = getDivision(tables[1], K)

np.savetxt('division.txt', division, '%d')
np.savetxt('C.txt', tables[0], '%f')
np.savetxt('J.txt', tables[1], '%d')













































































