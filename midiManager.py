from mido import MidiFile, MetaMessage
import time
import glob
import os
import music21
from collections import Counter

class MidiMan:

	def __init__(self, file):
		self.mid = MidiFile(file)
		self.file = file
		self.note_format = []
		self.lowerBound = 24
		self.upperBound = 102

	def showMidiMessage(self):
		for i, track in enumerate(self.mid.tracks):
			print('Track {}: {}'.format(i, track.name))
			for message in track:
				print(message)

	def make_Format(self):
		# make format ([(note.type,note)],time)
		for i, track in enumerate(self.mid.tracks):
			self.note_format = []
			note_list = []
			for message in track:
				if message.time != 0:
					if not note_list:
						pass
					elif note_list:
						# print (note_list)
						self.note_format += [(note_list,message.time)]
						note_list = []
					if message.type == 'note_on':
						note_list += [(message.type, message.note)]
					elif message.type == 'note_off':
						note_list += [(message.type, message.note)]
				elif message.time == 0:
					if message.type == 'note_on':
						note_list += [(message.type, message.note)]
					elif message.type == 'note_off':
						note_list += [(message.type, message.note)]
			if len(note_list) != 0:
				self.note_format += [(note_list,message.time)]

	def get_Note_Format(self):
		return self.note_format

	def show_Note_Format(self):
		print (self.note_format)

	def transpose(self):
		#converting everything into the key of C major or A minor

		# major conversions
		# majors = dict([("A-", 4),("A", 3),("B-", 2),("B", 1),("C", 0),("D-", -1),("D", -2),("E-", -3),("E", -4),("F", -5),("G-", 6),("G", 5)])
		# minors = dict([("A-", 1),("A", 0),("B-", -1),("B", -2),("C", -3),("D-", -4),("D", -5),("E-", 6),("E", 5),("F", 4),("G-", 3),("G", 2)])
		majors = dict([('A-', 4),('G#', 4),('A', 3),('A#', 2),('B-', 2),('B', 1),('C', 0),('C#', -1),('D-', -1),('D', -2),('D#', -3),('E-', -3),('E', -4),('F', -5),('F#', 6),('G-', 6),('G', 5)])
		minors = dict([('G#', 1), ('A-', 1),('A', 0),('A#', -1),('B-', -1),('B', -2),('C', -3),('C#', -4),('D-', -4),('D', -5),('D#', 6),('E-', 6),('E', 5),('F', 4),('F#', 3),('G-', 3),('G', 2)])
		
		#os.chdir("./")
		score = music21.converter.parse(self.file)
		key = score.analyze('key')
		print (key.tonic.name, key.mode)
		if key.mode == "major":
			halfSteps = majors[key.tonic.name]
	        
		elif key.mode == "minor":
			halfSteps = minors[key.tonic.name]
	    
		newscore = score.transpose(halfSteps)
		key = newscore.analyze('key')
		print (key.tonic.name, key.mode)
		newFileName = "C_" + self.file.split('/')[3]
		directoryPath = 'transposeDataSet/'+ self.file.split('/')[2]
		try:
			os.stat(directoryPath)
		except:
			os.mkdir(directoryPath)      
		newscore.write('midi',"transposeDataSet/"+self.file.split('/')[2]+'/'+newFileName)


	