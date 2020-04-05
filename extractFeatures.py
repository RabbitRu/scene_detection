import os

os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
import keras
import cv2
import numpy as np
import math

def _checkIndex(video, index):
	totalFrames = video.get(cv2.CAP_PROP_FRAME_COUNT)
	if index > totalFrames or index < 0:
		print('Кадр за границами видео')
		return False
	video.set(cv2.CAP_PROP_POS_FRAMES, index)
	return True

def readImageFromVideo(video, index):
	if(not _checkIndex(video,index)):
		return
	ret, frame = video.read()
	return frame




def kerasFeatureExtract(fv, shots, modelString, imageSize, shotParts, shotIndex):
	model = eval(modelString)
	predictedFrames = []
	width = imageSize
	height = imageSize
	for shot in shots:
		offset = ((shot[1] - shot[0]) * shotIndex) / shotParts
		try:
			imageIndex = shot[0] + offset
			frame = readImageFromVideo(fv, imageIndex)
			img = cv2.resize(frame,(width,height))
			reshapedImage = np.reshape(img,[1,width,height,3])
			middleFrame = model.predict(reshapedImage)
			predictedFrames.append(middleFrame[0])
		except Exception as e:
			print(e)
			print('Ошибка с получением особенностей шота, кадр ' + str(imageIndex))
	return predictedFrames



def HSVHistFeatureExtract(fv, shots, shotParts, shotIndex):
	predictedFrames = []
	for shot in shots:
		offset = ((shot[1] - shot[0]) * shotIndex) / shotParts
		try:
			imageIndex = shot[0] + offset
			image = readImageFromVideo(fv, imageIndex)
			hsvImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
			hist = cv2.calcHist([hsvImage],[0],None,[256],[0,256])
			unpackedHist = []
			for i in range(256):
				unpackedHist.append(hist[i][0])
			predictedFrames.append(unpackedHist)
		except Exception as e:
			print(e)
			print('Ошибка с получением особенностей шота, кадр ' + str(imageIndex))
	return predictedFrames
	return










































































