import os
import cv2
import numpy as np
import math
from scipy import spatial



def readData(folderPath):
	fs = open(folderPath + '\\shots.txt')
	#fv = cv2.VideoCapture(folderPath + '\\video.mp4')
	shots = readShots(fs)
	return shots#(shots, fv)

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

def main(args):
    # parse arguments using optparse or argparse 
    data = []
    for root, dirs, files in os.walk('./Datasets'):
    	#Номер означает что это одно из видео, а не подпапка
    	if(root[-1].isdigit()):
    		data.append(readData(root))

    print(data)

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])













































































