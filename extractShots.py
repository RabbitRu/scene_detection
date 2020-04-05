import sys
import ffmpeg
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
import tensorflow as tf
from TransNet2.transnet import TransNetParams, TransNet
from TransNet2.transnet_utils import draw_video_with_predictions, scenes_from_predictions

# initialize the network
def initTransNet():
	params = TransNetParams()
	params.CHECKPOINT_PATH = "./TransNet2/model/transnet_model-F16_L3_S2_D256"
	net = TransNet(params)
	return net, params;


def extractShotsTransNet(videoPath, net, params, debug = False):
	try:
		# export video into numpy array using ffmpeg
		video_stream, err = (
		    ffmpeg
		    .input(videoPath)
		    .output('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(params.INPUT_WIDTH, params.INPUT_HEIGHT))
		    .run(capture_stdout=True)
		)
		video = np.frombuffer(video_stream, np.uint8).reshape([-1, params.INPUT_HEIGHT, params.INPUT_WIDTH, 3])

		# predict transitions using the neural network
		predictions = net.predict_video(video)
		

		# Generate list of scenes from predictions, returns tuples of (start frame, end frame)
		#Это планы на самом деле
		scenes = scenes_from_predictions(predictions, threshold=0.1)
		return scenes
		# For ilustration purposes, only the visualized scenes are shown.
		#print(scenes)
	except Exception as e:
			print(e)

	return


