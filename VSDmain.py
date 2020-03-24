import os
import cv2
from enum import Enum
import numpy as np

import checkResults as cr
import detectScenes as ds 
import extractFeatures as ef 
import extractShots as es

class FeatureExtractionType(Enum):
	Basic = 1

#Строка начальный и конечный кадр
def readScenesIBM(fscenes, shots):
	scenes = np.loadtxt(fscenes, int)
	#array = [0]
	#with open(fscenes) as f:
	#    lines=f.readlines()
	#    for line in lines:
	#        endingFrame = int(line.split()[0])
	#        planIndex = next(i for i, x in enumerate(shots) if endingFrame == x[1])
	#    array.append(planIndex)
	return scenes

#Через запятую номера планов первых в сцене, переводим в кадры 
def readScenesBBC(fscenes, shots):
	scenes = np.loadtxt(fscenes, int,  delimiter=',' )
	scenesByFrames = []
	for i in range(1, len(scenes)):
		scenesByFrames.append([shots[scenes[i - 1]][0], shots[scenes[i] - 1][1]])
	return scenesByFrames

def readScenes(fscenes, shots):
	scenesByFrames = []
	with open(fscenes) as f:
	    lines=f.readlines()
	    for line in lines:
	        scenesByFrames.append(
	        	[shots[int(line.split()[0])][0],
	        	shots[int(line.split()[-1])][1]])
	#array = []
	#with open(fscenes) as f:
	#    lines=f.readlines()
	#    for line in lines:
	#        array.append(int(line.split()[0]))
	#    array.append(int(lines[-1].split()[-1]) + 1)
	return scenesByFrames

#Строка перечисление планов в сцене
def readShots(shotFile):
	shots = np.loadtxt(shotFile, int)
	array = []
	for shot in shots: # read rest of lines
		array.append([shot[0],shot[1]])
	return array

def readDivision(fdivision):
	division = np.loadtxt(fdivision, int)
	return division

def readFeatures(ffeatures):
	features = np.loadtxt(ffeatures, int)
	return features

def saveFeatures(ffeatures, features):
	np.savetxt(ffeatures, features, fmt='%.10f')
	pass

def saveDivision(fdivision, fdivisionByFrames, division, saveDivisionByShots = True):
	np.savetxt(fdivisionByFrames, division[0], fmt='%d')
	if(saveDivisionByShots):
		np.savetxt(fdivision, division[1], fmt='%d')
	pass

def saveMetrics(fmetrics, metrics):
	np.savetxt(fmetrics, metrics, fmt='%s')
	pass

def saveScenesByFrames(fscenes, scenes):
	np.savetxt(fscenes, scenes, fmt='%d')
	pass

def saveShots(fshots, shots):
	np.savetxt(fshots, shots, fmt='%d')
	pass

def readData(
	folderPath, generateShots, generateDiviion, generateFeatures,
	shotNet, saveScenesByFramesToFile, featureExtractionType):
	#print(1)
	print(folderPath)
	featureFolderPath = folderPath + '\\' + featureExtractionType.name
	
	videoname = '\\video.mp4'
	try:
		fv = cv2.VideoCapture(folderPath + '\\video.mp4')
		if(not fv.isOpened()):
			videoname = '\\video.mkv'
			fv = cv2.VideoCapture(folderPath + '\\video.mkv')
		if(not fv.isOpened()):
			videoname = '\\video.avi'
			fv = cv2.VideoCapture(folderPath + '\\video.avi')
		if(not fv.isOpened()):
			videoname = '\\video.mov'
			fv = cv2.VideoCapture(folderPath + '\\video.mov')
		fv.get(cv2.CAP_PROP_FRAME_COUNT)
	except Exception as e:
		print(e)
		print("В папке " + str(folderPath) + " нет видео")
		return

	#print(2)
	try:
		fshots = folderPath + '\\shots.txt'
		if(not generateShots):
			shots = readShots(fshots)
		else:
			shots = es.extractShotsTransNet(folderPath + videoname, shotNet[0], shotNet[1])
			saveShots(fshots,shots)
	except Exception as e:
		print(e)
		try:
			print("В папке " + str(folderPath) + " нет файла шотов, генерируем")
			shots = es.extractShotsTransNet(folderPath + videoname, shotNet[0], shotNet[1])
			saveShots(fshots,shots)
		except Exception as e:
			print(e)

	#print(3)
	try:
		if(featureExtractionType == FeatureExtractionType.Basic):
			ffeatures = featureFolderPath + '\\features.txt'
		if(not generateFeatures):
			features = readFeatures(ffeatures)
		else:
			if(featureExtractionType == FeatureExtractionType.Basic):
				features = ef.basicFeatureExctract(fv, shots)
			saveFeatures(ffeatures, features)
	except Exception as e:
		print(e)
		print("В папке " + str(folderPath) + " нет файла особеностей, пробуем сгенерировать")
		features = ef.basicFeatureExctract(fv, shots)
		saveFeatures(ffeatures, features)


	#print(4)
	try:		
		fscenes = folderPath + '\\scenes.txt'
		fscenesByFrames = folderPath + '\\scenesByFrames.txt'
		#Не у всего есть разбиение сцен на планы, так что работаем с разбиением по кадрам
		if('IBM' in folderPath):
			scenes = readScenesIBM(fscenes, shots)
		elif('BBC' in folderPath):
			scenes = readScenesBBC(fscenes, shots)
		else:
			scenes = readScenes(fscenes, shots)
		if saveScenesByFramesToFile:
			saveScenesByFrames(fscenesByFrames, scenes)
	except Exception as e:
		print(e)
		print("В папке " + str(folderPath) + " нет файла оригинальных сцен, не сможем провести сравнение результатов")
		return

	#print(5)
	try:
		fdivision = folderPath + '\\division.txt'
		fdivisionByScenes = folderPath + '\\divisionByFrames.txt'
		if(not generateDiviion):
			division = readDivision(fdivisionByScenes)
		else:
			#[divisionByFrames, division]
			divisions = ds.basicSceneDetect(features, shots, len(scenes), len(shots))
			division = divisions[0]
			saveDivision(fdivision, fdivisionByScenes, divisions)
	except Exception as e:
		print(e)
		print("В папке " + str(folderPath) + " нет файла нашего разбиения, пробуем сгенерировать")
		divisions = ds.basicSceneDetect(features, shots, len(scenes), len(shots))
		division = divisions[0]
		saveDivision(fdivision, fdivisionByScenes, divisions)

	#print(6)
	try:		
		fmetrics = folderPath + '\\metrics.txt'
		metrics = cr.getMetrics(scenes, division)
		saveMetrics(fmetrics, metrics)
	except Exception as e:
		print(e)
		print("В папке " + str(folderPath) + " не получилось провести сравнение")

	return True

def main(args):
	# parse arguments using optparse or argparse 
    data = []
    shotNet = es.initTransNet()
    try:
	    for root, dirs, files in os.walk('./Datasets'):
	    #Номер означает что это одно из видео, а не подпапка
	    	try:
	    		if(root[-1].isdigit()):
	    			data.append(
	    				readData(
	    					root, False, False, False, shotNet, True,
	    					FeatureExtractionType.Basic))
	    	except Exception as e:
	    		print(e)
    except Exception as e:
    	print(e)

   # print(data)

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])













































































