import sys
import ffmpeg
import numpy as np
import tensorflow as tf
from TransNet2.transnet import TransNetParams, TransNet
from TransNet2.transnet_utils import draw_video_with_predictions, scenes_from_predictions

# initialize the network

def extractShotsTransNet(videoPath):
	try:
		print(0)
		params = TransNetParams()
		params.CHECKPOINT_PATH = "./model/transnet_model-F16_L3_S2_D256"
		net = TransNet(params)
		print(1)

		# export video into numpy array using ffmpeg
		video_stream, err = (
		    ffmpeg
		    .input(videoPath)
		    .output('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(params.INPUT_WIDTH, params.INPUT_HEIGHT))
		    .run(capture_stdout=True)
		)
		video = np.frombuffer(video_stream, np.uint8).reshape([-1, params.INPUT_HEIGHT, params.INPUT_WIDTH, 3])

		print(2)
		# predict transitions using the neural network
		predictions = net.predict_video(video)
		print(3)
		return predictions

		# Generate list of scenes from predictions, returns tuples of (start frame, end frame)
		#scenes = scenes_from_predictions(predictions, threshold=0.1)

		# For ilustration purposes, only the visualized scenes are shown.
		#print(scenes)
	except Exception as e:
			print(e)

	print(4)
	return


