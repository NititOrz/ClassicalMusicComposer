from preprocess import Transpose, PrepareData
from model import Model
from predictor import Predictor
from midiManager import MidiMananger
import numpy as np
import glob

# train mode 1=single file, 2=all dataset
# transpose mode 3
def mode(mode):
	# train 1 file
	window_size = 20
	if mode == "1":
		# file = './transposeDataSet/bach/C_bach_850_format0.mid'
		file = './transposeDataSet/bach/C_bach_847_format0.mid'
		# file = './transposeDataSet/chopin/C_chpn_op10_e12_format0.mid'
		# file = './transposeDataSet/chopin/C_chpn-p10_format0.mid'
		# file = './new_song.mid'
		print("Preparing Data.....")
		prepare = PrepareData()
		prepare.buildCorpus(file)
		trainX, trainY = prepare.buildXY(window_size)
		# print(trainX)
		prepare.save_data()

		m = Model()
		m.createModel(trainX ,trainY)
		m.compileModel()
		m.trainModel(trainX, trainY)
		m.save_model()
		m.testModel(trainX, trainY)

		# model = "./model/model.json"
		# weights = "./model/model.h5"
		# m.load_model(model, weights)

	# train all files
	elif mode == "2":
		print("Preparing Data.....")
		prepare = PrepareData()
		for file in glob.iglob('./transposeDataSet/bach/*.mid'):
			prepare.buildCorpus(file)
		trainX, trainY = prepare.buildXY(window_size)
		prepare.save_data()

		m = Model()
		m.createModel(trainX ,trainY)
		m.compileModel()
		m.trainModel(trainX, trainY)
		m.save_model()
		m.testModel(trainX, trainY)
		# model = "./model/model.json"
		# weights = "./model/model.h5"
		# m.load_model(model, weights)

	# test model
	elif mode == "3":
		# file = './transposeDataSet/bach/C_bach_850_format0.mid'
		# file = './transposeDataSet/bach/C_bach_847_format0.mid'
		# file = './transposeDataSet/chopin/C_chpn_op10_e12_format0.mid'
		# file = './transposeDataSet/chopin/C_chpn-p10_format0.mid'
		# file = "./SONG.mid"
		for file in glob.iglob('./transposeDataSet/bach/*.mid'):
			prepare = PrepareData()
			prepare.buildCorpus(file)
			testX , testY = prepare.buildXY(window_size)
			m = Model()
			model = "./model/model.json"
			weights = "./model/model.h5"
			m.load_model(model,weights)
			m.compileModel()
			m.testModel(testX ,testY)

	# transpose midi
	elif mode == "4":
		for file in glob.iglob('./DataSet/*/*.mid'):
			t = Transpose(file)
			t.transpose()

	# predict
	elif mode == "5":
		prepare = PrepareData()
		
		dataX = prepare.load_dataX()
		# print(len(dataX))
		dist_time1, dist_time2 = prepare.load_dist_time()
		# print(dist_time)

		m = Model()
		model = "./model/model.json"
		weights = "./model/model.h5"
		m.load_model(model,weights)

		p = Predictor(m.get_model())
		p.predict_on_corpus(dataX, window_size)
		type_and_note = p.buildNotetype()
		song = p.buildSong(type_and_note, dist_time1, dist_time2)


		midi = MidiMananger()
		midi.creatMidiSong(song)
		print("Created Song!! name: Song.midi")

	else:
		print("your selecting mode is not found!!!")
	

if __name__ == '__main__':
	print("please select mode...")
	print("training mode: 1=single file , 2=all dataset")
	print("3 = test model")
	print("4 = transpose mode")
	print("5 = load_model and create song")
	m = input()
	# mode = "2"
	mode(m)
