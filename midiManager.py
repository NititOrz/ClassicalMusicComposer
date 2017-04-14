from mido import MidiFile, MetaMessage
import time
import glob
import os
import music21

class MidiMan:

	def __init__(self, file):
		self.mid = MidiFile(file)
		self.file = file
		self.note_format = []
		self.lowerBound = 24
		self.upperBound = 102
		self.cumTime = 0

	def showMidiMessage(self):
		for i, track in enumerate(self.mid.tracks):
			print('Track {}: {}'.format(i, track.name))
			for message in track:
				if message.type == 'note_on':
					print(message)
				elif message.type == 'note_off':
					print(message)

	def make_Format(self):
		# make format ([(note.type,note)],time)
		for i, track in enumerate(self.mid.tracks):
			self.note_format = []
			note_list = []
			temp = 0
			isfirst = True
			for message in track:
				if message.time != 0:
					#set first message time to 0
					if isfirst:
						self.cumTime = 0
						if message.type == 'note_on':
							isfirst = False
					else:
						self.cumTime += message.time
						print
					#make note_format
					if not note_list:
						pass
					elif note_list:
						# print (note_list)
						self.note_format += [(note_list, self.cumTime-message.time)]
						# self.note_format += [(note_list, self.cumTime-message.time-temp)]
						# temp = self.cumTime - message.time
						note_list = []
					if message.type == 'note_on':
						if message.note <= self.upperBound and message.note >= self.lowerBound:
							note_list += [(message.type, message.note)]
					elif message.type == 'note_off':
						if message.note <= self.upperBound and message.note >= self.lowerBound:
							note_list += [(message.type, message.note)]
				elif message.time == 0:
					if message.type == 'note_on':
						note_list += [(message.type, message.note)]
					elif message.type == 'note_off':
						note_list += [(message.type, message.note)]
			if len(note_list) != 0:
				# self.note_format += [(note_list, self.cumTime)]
				self.note_format += [(note_list, self.cumTime-message.time-temp)]
				# print (self.cumTime)

	def get_Note_Format(self):
		return self.note_format

	def show_Note_Format(self):
		print (self.note_format)

	def get_Cum_Time(self):
		return self.cumTime

	


	