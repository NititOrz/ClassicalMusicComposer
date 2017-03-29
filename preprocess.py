from mido import MidiFile, MetaMessage
import numpy as np
import time
import glob
import os
import music21

lowerBound = 24
upperBound = 102

class PreProcessData(object):
	
	def __init__(self, note_format):
		self.time = note_format[0][1]
		self.EOT = note_format[len(note_format)-1][1]
		self.note_format = note_format
		self.countNote = 0
		firstState = [0]*(upperBound-lowerBound+1+4)
		self.note_sheet = np.array(firstState)
		
	def buildBeat(self, time):
		beat = [2*x-1 for x in [time%2, (time//2)%2, (time//4)%2, (time//8)%2]]
		# print (beat)
		return beat

	def buildNoteMatrix(self, note):
		noteMatrix = [0]*(upperBound-lowerBound+1)
		for i in range(0, len(note)):
			if note[i][0] == 'note_on':
				noteMatrix[note[i][1]-lowerBound] = 1
			elif note[i][0] == 'note_off':
				noteMatrix[note[i][1]-lowerBound] = -1
			# print (noteMatrix)
		return noteMatrix

	def make_Note_Sheet(self):
		for i in range(self.time, self.EOT+1):
			if self.note_format[self.countNote][1] == i:
				state = self.buildNoteMatrix(self.note_format[self.countNote][0]) + self.buildBeat(self.time)
				self.note_sheet = np.vstack((self.note_sheet, state))
				self.countNote += 1
			else:
				state = self.buildNoteMatrix([]) + self.buildBeat(self.time)
				self.note_sheet = np.vstack((self.note_sheet, state))
			self.time += 1

	def get_Note_Sheet(self):
		return self.note_sheet
