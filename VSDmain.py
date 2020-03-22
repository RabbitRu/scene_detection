import os
import cv2
import numpy as np

import checkResults as cr
import detectScenes as ds 
import extractFeatures as ef 
import extractShots as es

#Строка начальный и конечный кадр
def readScenesIBM(fscenes, shots):
	array = [0]
	with open(fscenes) as f:
	    lines=f.readlines()
	    for line in lines:
	        endingFrame = int(line.split()[0])
	        planIndex = next(i for i, x in enumerate(shots) if endingFrame == x[1])
	    array.append(planIndex)
	return array

#Через запятую номера планов первых в сцене
def readScenesBBC(fscenes, shots):
	scenes = np.loadtxt(fscenes, int,  delimiter=',' )
	return scenes

def readScenes(fscenes, shots):
	array = []
	with open(fscenes) as f:
	    lines=f.readlines()
	    for line in lines:
	        array.append(int(line.split()[0]))
	    array.append(int(lines[-1].split()[-1]) + 1)
	return array

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
	np.savetxt(ffeatures, features)
	pass

def saveDivision(fdivision, division):
	np.savetxt(fdivision, division)
	pass

def saveMetrics(fmetrics, metrics):
	np.savetxt(fmetrics, metrics)
	pass

def readData(folderPath, generateShots, generateDiviion, generateFeatures):
	#print(1)
	print(folderPath)
	videoname = '\\video.mp4'
	try:
		fv = cv2.VideoCapture(folderPath + '\\video.mp4')
		if(not fv.isOpened()):
			videoname = '\\video.mkv'
			fv = cv2.VideoCapture(folderPath + '\\video.mkv')
		elif(not fv.isOpened()):
			videoname = '\\video.avi'
			fv = cv2.VideoCapture(folderPath + '\\video.avi')
		elif(not fv.isOpened()):
			videoname = '\\video.mov'
			fv = cv2.VideoCapture(folderPath + '\\video.mov')
		fv.get(cv2.CAP_PROP_FRAME_COUNT)
	except Exception as e:
		print(e)
		print("В папке " + str(folderPath) + " нет видео")
		return

	#print(2)
	try:
		if(not generateShots):
			shots = readShots(folderPath + '\\shots.txt')
		else:
			shots = es.extractShotsTransNet(folderPath + videoname)
	except Exception as e:
		print(e)
		try:
			print("В папке " + str(folderPath) + " нет файла шотов, генерируем")
			shots = es.extractShotsTransNet(folderPath + videoname)
		except Exception as e:
			print(e)

	#print(3)
	try:
		ffeatures = folderPath + '\\features.txt'
		if(not generateFeatures):
			features = readFeatures(ffeatures)
		else:
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
		if('IBM' in folderPath):
			scenes = readScenesIBM(fscenes, shots)
		elif('BBC' in folderPath):
			scenes = readScenesBBC(fscenes, shots)
		else:
			scenes = readScenes(fscenes, shots)
	except Exception as e:
		print(e)
		print("В папке " + str(folderPath) + " нет файла оригинальных сцен, не сможем провести сравнение результатов")
		return

	#print(5)
	try:
		fdivision = folderPath + '\\division.txt'
		if(not generateDiviion):
			division = readDivision(fdivision)
		else:
			division = ds.basicSceneDetect(features, len(scenes), len(shots))
			saveDivision(fdivision, division)
	except Exception as e:
		print(e)
		print("В папке " + str(folderPath) + " нет файла нашего разбиения, пробуем сгенерировать")
		division = ds.basicSceneDetect(features, len(scenes), len(shots))
		saveDivision(fdivision, division)

	#print(6)
	try:		
		fmetrics = folderPath + '\\metrics.txt'
		metrics = cr.getMetrics(scenes, division)
		saveMetrics(fmetrics, metrics)
	except Exception as e:
		print(e)
		print("В папке " + str(folderPath) + " не получилось провести сравнение")

	return (shots, fv)

def main(args):
	# parse arguments using optparse or argparse 
    data = []
    try:
	    for root, dirs, files in os.walk('./Datasets'):
	    #Номер означает что это одно из видео, а не подпапка
	    		if(root[-1].isdigit()):
	    			data.append(readData(root, False, False, False))
    except Exception as e:
    	print(e)

   # print(data)

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])













































































