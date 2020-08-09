

import VSDmain as vsd
import extractShots as es 





def analitScenes(folderPath):
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







def main(args):
	# parse arguments using optparse or argparse 
	shotNet = es.initTransNet()
	try:
		for root, dirs, files in os.walk('./Datasets'):
		#Номер означает что это одно из видео, а не подпапка
			try:
				if(root[-1].isdigit()):
					analitScenes(root)
					
			except Exception as e:
				print(e)
	except Exception as e:
		print(e)

	# print(data)

if __name__ == '__main__':
	import sys
	main(sys.argv[1:])