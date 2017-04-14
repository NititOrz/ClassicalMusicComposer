from midiManager import MidiMan
from preprocess import BuildNoteSheet, Transpose
from model import Model
from predictor import Predictor
import numpy as np
import glob

# train mode 1=single file, 2=all dataset
# transpose mode 3
def file_mode(mode, model):
	if mode == "1":
		# file = './transposeDataSet/bach/C_bach_850_format0.mid'
		file = './new_song.mid'
		run(file, model)

	elif mode == "2":
		for file in glob.iglob('./transposeDataSet/*/*.mid'):
			run(file, model)

	elif mode == "3":
		for file in glob.iglob('./DataSet/*/*.mid'):
			t = Transpose(file)
			t.transpose()
	else:
		print("your selecting mode is not found!!!")

def run(file, model):

	# make easy format
	m = MidiMan(file)
	m.make_Format()
	note_format = m.get_Note_Format()
	cumTime = m.get_Cum_Time()
	# m.show_Note_Format()
	# m.showMidiMessage()

	X,Y = mo.init_data()
	countNote = 0
	for time in range(0, cumTime+1):
		# make note matrix
		print ("-----------------Time: {}/{}----------------".format(time, cumTime))
		if time == note_format[countNote][1]:
			print ("********************* Change *****************")
			BS = BuildNoteSheet(note_format[countNote][0], Y)
			countNote += 1

		Y = BS.buildNoteMatrix()

		# # make model
		mo.make_data(Y)
		mo.fit_model()
		mo.slide_window()

	# mo.summarize()
	mo.save_model()
	# # predict
	# p = Predictor(model)
	# p.predict()
	

if __name__ == '__main__':
	print("please select mode...")
	print("training mode: 1=single file , 2=all dataset")
	print("transpose mode = 3")
	# mode = input()
	mo = Model()
	mo.create_model()
	mode = "1"
	file_mode(mode, mo)
