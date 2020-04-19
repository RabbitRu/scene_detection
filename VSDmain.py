import os
import cv2
from enum import Enum
import numpy as np

import checkResults as cr
import detectScenes as ds 
import extractFeatures as ef 
import extractShots as es

class FeatureType(Enum):
	Xception = 0
	VGG19 = 1
	InceptionV3 = 2
	InceptionResNetV2 = 3
	MobileNet = 4
	MobileNetV2 = 5
	DenseNet = 6
	NASNet = 7
	AllKeras = 8
	HSV = 21
	Audio = 31
	ALL=100


#ResNet, inceptionResNet оч плохие результаты, а VGG16 оч похож на VGG19 
#это для AMD
#kerasModels = [
#	"keras.applications.xception.Xception(include_top=False, weights='imagenet', pooling='avg')",#299
#	"keras.applications.vgg19.VGG19(include_top=False, weights='imagenet', pooling='avg')",#224
#	"keras.applications.inception_v3.InceptionV3(include_top=False, weights='imagenet', pooling='avg')",#299
#	"keras.applications.mobilenet.MobileNet(input_shape=(224, 224, 3),include_top=False, weights='imagenet', pooling='avg')",#224
#	"keras.applications.mobilenet_v2.MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet', pooling='avg')",#224
#	"keras.applications.densenet.DenseNet201(include_top=False, weights='imagenet', pooling='avg')",#224
#	"keras.applications.nasnet.NASNetLarge(include_top=False, weights='imagenet', pooling='avg')"#224
#	]

kerasModels = [
	"tensorflow.keras.applications.xception.Xception(include_top=False, weights='imagenet', pooling='avg')",#299
	"tensorflow.keras.applications.vgg19.VGG19(include_top=False, weights='imagenet', pooling='avg')",#224
	"tensorflow.keras.applications.inception_v3.InceptionV3(include_top=False, weights='imagenet', pooling='avg')",#299
	"tensorflow.keras.applications.mobilenet.MobileNet(input_shape=(224, 224, 3),include_top=False, weights='imagenet', pooling='avg')",#224
	"tensorflow.keras.applications.mobilenet_v2.MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet', pooling='avg')",#224
	"tensorflow.keras.applications.densenet.DenseNet201(include_top=False, weights='imagenet', pooling='avg')",#224
	"tensorflow.keras.applications.nasnet.NASNetLarge(include_top=False, weights='imagenet', pooling='avg')"#224
	]

kerasImageSize = [
299,224,299,
224,224,224,331]


#Строка начальный и конечный кадр
def readScenesIBM(fscenes, shots):
	scenes = np.loadtxt(fscenes, int)
	#array = [0]
	#with open(fscenes) as f:
	#	lines=f.readlines()
	#	for line in lines:
	#		endingFrame = int(line.split()[0])
	#		planIndex = next(i for i, x in enumerate(shots) if endingFrame == x[1])
	#	array.append(planIndex)
	return scenes

#Через запятую номера планов первых в сцене, переводим в кадры 
def readScenesBBC(fscenes, shots):
	scenes = np.loadtxt(fscenes, int, delimiter=',' )
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
	#	lines=f.readlines()
	#	for line in lines:
	#		array.append(int(line.split()[0]))
	#	array.append(int(lines[-1].split()[-1]) + 1)
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
	features = np.loadtxt(ffeatures + '.txt', int)
	return features

def saveFeatures(ffeatures, features):
	np.savetxt(ffeatures + '.txt', features, fmt='%.10f')
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
	shotNet, saveScenesByFramesToFile, featureType, shotParts,
	shotIndex):
	#print(1)
	print(folderPath)
	
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
		ffeaturesShort = folderPath + '\\features'
		#shotIndex
		if(not generateFeatures):
			if(featureType != FeatureType.ALL and featureType != FeatureType.AllKeras):
				features = readFeatures(ffeaturesShort + featureType.name + '.txt')
		else:
			if(featureType.value < len(kerasModels)):
				features = ef.kerasFeatureExtract(fv, shots, kerasModels[featureType.value],
					kerasImageSize[featureType.value], shotParts, shotIndex)

			elif(featureType == FeatureType.ALL):
				for i in range(len(kerasModels)):
					print(FeatureType(i).name)
					features = ef.kerasFeatureExtract(fv, shots, kerasModels[i],
					kerasImageSize[i], shotParts, shotIndex)
					saveFeatures(ffeaturesShort + FeatureType(i).name, features)

				features = ef.HSVHistFeatureExtract(fv, shots, shotParts, shotIndex)
				saveFeatures(ffeaturesShort + featureType.HSV.name, features)

			elif(featureType == FeatureType.HSV):
				features = ef.HSVHistFeatureExtract(fv, shots, shotParts, shotIndex)

			if(featureType != FeatureType.ALL):
				saveFeatures(ffeaturesShort + featureType.name, features)

	except Exception as e:
		print(e)
		print("В папке " + str(folderPath) + " нет файла особеностей, пробуем сгенерировать")
		#Добавить для всего
		if(featureType.value < len(kerasModels)):
			features = ef.kerasFeatureExtract(fv, shots, kerasModels[featureType.value],
					kerasImageSize[featureType.value], shotParts, shotIndex)
		elif(featureType == FeatureType.HSV):
				features = ef.HSVHistFeatureExtract(fv, shots, shotParts, shotIndex)
		saveFeatures(ffeaturesShort + featureType.name , features)


	#print(4)
	try:		
		fscenes = folderPath + '\\scenes.txt'
		fscenesByFrames = folderPath + '\\scenesByFrames.txt'
		#Не у всего есть разбиение сцен на планы, так что работаем с разбиением по кадрам
		if('IBM' in folderPath or 'RAI' in folderPath):
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
		fdivision = folderPath + '\\division' + featureType.name +'.txt'
		fdivisionByFrames = folderPath + '\\divisionByFrames' + featureType.name +'.txt'
		fmatrix = folderPath + '\\' + featureType.name 
		if(not generateDiviion):
			if(featureType != FeatureType.ALL):
				division = readDivision(fdivisionByFrames)
		else:
			#[divisionByFrames, division]
			if(featureType == FeatureType.ALL):

				for i in range(len(kerasModels)):
					fmatrix = folderPath + '\\' + FeatureType(i).name 
					features = readFeatures(ffeaturesShort + FeatureType(i).name)
					divisions = ds.basicSceneDetect(features, shots, len(scenes), len(shots), fmatrix)
					division = divisions[0]
					saveDivision(folderPath + '\\division' + FeatureType(i).name +'.txt', 
						 folderPath + '\\divisionByFrames' + FeatureType(i).name +'.txt', divisions)
				
				fmatrix = folderPath + '\\' + featureType.HSV.name
				features = readFeatures(ffeaturesShort + featureType.HSV.name)
				divisions = ds.basicSceneDetect(features, shots, len(scenes), len(shots), fmatrix)
				division = divisions[0]
				saveDivision(folderPath + '\\division' + FeatureType(i).name +'.txt', 
					 folderPath + '\\divisionByFrames' + FeatureType(i).name +'.txt', divisions)

			elif(featureType == FeatureType.AllKeras):
				matrixs = []
				for i in range(len(kerasModels)):
					features = readFeatures(ffeaturesShort + FeatureType(i).name)
					divisions = ds.basicSceneDetect(features, shots, len(scenes), len(shots), "None")
					matrixs.append(divisions[2])

				for i in range(1,len(matrixs)):
					for j in range(len(matrixs[0])):
						for k in range(len(matrixs[0][0])):
							matrixs[0][j][k] = float(matrixs[0][j][k]) + float(matrixs[i][j][k])

				fmatrix = folderPath + '\\' + featureType.name 
				divisions = ds.basicSceneDetectWInputMatrix(features, shots,
				 len(scenes), len(shots), fmatrix, matrixs[0])	
				division = divisions[0]
				saveDivision(folderPath + '\\division' + featureType.name +'.txt', 
					 folderPath + '\\divisionByFrames' + featureType.name +'.txt', divisions)

			else:
				divisions = ds.basicSceneDetect(features, shots, len(scenes), len(shots), fmatrix)
				division = divisions[0]
				saveDivision(fdivision, fdivisionByFrames, divisions)
	except Exception as e:
		print(e)
		print("В папке " + str(folderPath) + " нет файла нашего разбиения, пробуем сгенерировать")
		divisions = ds.basicSceneDetect(features, shots, len(scenes), len(shots), fmatrix)
		division = divisions[0]
		saveDivision(fdivision, fdivisionByFrames, divisions)

	#print(6)
	try:		
		fmetrics = folderPath + '\\metrics' + featureType.name + '.txt'
		
		if(featureType == FeatureType.ALL):
			for i in range(len(kerasModels)):
				fmetrics = folderPath + '\\metric' + FeatureType(i).name + '.txt'#'_' + str(shotParts) + '_' + str(shotIndex)
					
				division = readDivision(folderPath + '\\divisionByFrames' + FeatureType(i).name +'.txt')

				metrics = cr.getMetrics(scenes, division)
				saveMetrics(fmetrics, metrics)
			
			fmetrics = folderPath + '\\metric' + featureType.HSV.name +'.txt'

			division = readDivision(folderPath + '\\divisionByFrames' + featureType.HSV.name +'.txt')

			metrics = cr.getMetrics(scenes, division)
			saveMetrics(fmetrics, metrics)
			
		else:
			metrics = cr.getMetrics(scenes, division)
			saveMetrics(fmetrics, metrics)
	except Exception as e:
		print(e)
		print("В папке " + str(folderPath) + " не получилось провести сравнение")

	return True

def main(args):
	# parse arguments using optparse or argparse 
	shotNet = es.initTransNet()
	try:
		for root, dirs, files in os.walk('./Datasets'):
		#Номер означает что это одно из видео, а не подпапка
			try:
				if(root[-1].isdigit()):
					readData(
						root, False, True, True,
						shotNet, False,	FeatureType.ALL, 2,
						1)# Опыт показал что выбор разных кадров из одного шота слабо что-то меняет
					#	folderPath, generateShots, generateDiviion, generateFeatures,
					#	shotNet, saveScenesByFramesToFile, featureExtractionType, shotParts,
					#	shotIndex):
					
			except Exception as e:
				print(e)
	except Exception as e:
		print(e)

	# print(data)

if __name__ == '__main__':
	import sys
	main(sys.argv[1:])













































































