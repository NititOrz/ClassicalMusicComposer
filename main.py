from midiManager import MidiMan
from preprocess import PreProcessData

if __name__ == '__main__':
	# #use all dataset
	# for file in glob.iglob('./transposeDataSet/*/*.mid'):
	# 	m = MidiMan(file)
	# 	print(file.split('/')[3])
	#     # transpose midi to key C   
	# 	m.transpose()

	#use 1 test dataset
	# file = './transposeDataSet/bach/C_bach_850_format0.mid'
	file = './new_song.mid'

	m = MidiMan(file)
	m.make_Format()
	note_format = m.get_Note_Format()
	m.show_Note_Format()
	# print(note_format[3][0])

	p = PreProcessData(note_format)
	p.make_Note_Sheet()
	note_Sheet = p.get_Note_Sheet()
	for x in note_Sheet:
		print (x)
	# print(note_format[len(note_format)-1][1])
	# m.showMessage()