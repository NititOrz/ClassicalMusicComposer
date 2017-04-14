from mido import MidiFile, MetaMessage
import glob
import os
import time
import numpy as np
import music21

lowerBound = 24
upperBound = 102

class Transpose(object):

	def __init__(self, file):
		self.file = file

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
		newFileName = "C_" + self.file.split('/')[len(self.file.split('/'))-1]
		try:
			directoryPath = 'transposeDataSet/'+ self.file.split('/')[2]
		except:
			directoryPath = 'transposeDataSet/'
		try:
			os.stat(directoryPath)
		except:
			os.mkdir(directoryPath)
		
		try:
			newscore.write('midi',"transposeDataSet/"+self.file.split('/')[2]+'/'+newFileName)
		except:      
			newscore.write('midi',"transposeDataSet/"+'/'+newFileName)
		


class BuildNoteSheet(object):
	
	def __init__(self, note_format, curentState):
		# self.time = note_format[0][1]
		# self.EOT = note_format[len(note_format)-1][1]
		self.note = note_format
		self.noteMatrix = curentState
		# self.countNote = 0
		# firstState = [0]*(upperBound-lowerBound+4)
		# self.note_sheet = np.array(firstState)
		# self.timeEOT = cumTime
		
	# def buildBeat(self, time):
	# 	# beat = [2*x-1 for x in [time%2, (time//2)%2, (time//4)%2, (time//8)%2]]
	# 	beat = [time%2, (time//2)%2, (time//4)%2, (time//8)%2]
	# 	# print (beat)
	# 	return beat

	def buildNoteMatrix(self):
		for i in range(0, len(self.note)):
			if self.note[i][0] == 'note_on':
				self.noteMatrix[0][self.note[i][1]-lowerBound-1] = 1
			elif self.note[i][0] == 'note_off':
				self.noteMatrix[0][self.note[i][1]-lowerBound-1] = 0
				# print (noteMatrix)

		return self.noteMatrix


	# [0-78]Note, [79-82]beats/sampling, 	
	# def make_Note_Sheet(self):
	# 	for i in range(self.time, self.EOT):
	# 		if self.note_format[self.countNote][1] == i:
	# 			state = self.buildNoteMatrix(self.note_format[self.countNote][0]) + self.buildBeat(self.time)
	# 			self.note_sheet = np.vstack((self.note_sheet, state))
	# 			self.countNote += 1
	# 		else:
	# 			state = self.buildNoteMatrix([]) + self.buildBeat(self.time)
	# 			self.note_sheet = np.vstack((self.note_sheet, state))
	# 		self.time += 1

		# for i in range(0,len(self.note_format)):
		# 	# print(self.note_format[i])
		# 	state = self.buildNoteMatrix(self.note_format[i][0]) + self.buildBeat(self.note_format[i][1])
		# 	self.note_sheet = np.vstack((self.note_sheet, state))

		# end_state = [0]*((upperBound-lowerBound)+4)
		# self.note_sheet = np.vstack((self.note_sheet, end_state))

	# def get_Note_Sheet(self):
	# 	return self.note_sheet
