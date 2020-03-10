import os

os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
import keras
import cv2
import numpy as np
import math

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


def basicFeatureExctract(fv, shots):
	model = keras.applications.xception.Xception(include_top=False, weights='imagenet', pooling='avg')
	predictedFrames = []
	for shot in shots:
		imageIndex = (shot[0] + shot[1]) / 2
		image = readImageFromVideo(fv, imageIndex)
		middleFrame = model.predict(image)
		predictedFrames.append(middleFrame[0])
	return predictedFrames













































































