import numpy as np
import os
import h5py
from mido import Message, MidiFile, MidiTrack, MetaMessage
from keras.preprocessing.sequence import pad_sequences
import time
import glob
import pickle
import music21

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
		


class PrepareData(object):
	def __init__(self):
		self.dist_time1 = {}
		self.dist_time1[-1] = {}
		self.dist_time1[-1][-1] = {}
		self.dist_time1[-1][-1][-1] = {}
		self.dist_time2 = {}
		self.dist_time2[-1] = {}
		self.dist_time2[-1][-1] = {}

		dataX = []
		dataY =[]
		self.note = []
		self.timelist = []
		self.note_type = []
		self.dataX = []
		self.dataY =[]

	def buildCorpus(self, file):
		self.note.append(-1)
		self.note_type.append(-1)
		self.timelist.append(-1)
		mid = MidiFile(file)
		for i, track in enumerate(mid.tracks):
			for message in track:
				time = message.time
				if message.time >= 4096:
					time = 4096
				if message.type == 'note_on':
					self.note_type.append(1)
					self.note.append(message.note)
					self.timelist.append(time)
				elif message.type == 'note_off':
					self.note.append(message.note)
					self.note_type.append(1)
					self.timelist.append(time)

		for i in range(1,len(self.note)):
			if self.note[i-1] == -1:
				pass
			else:
				if self.note[i-1] in self.dist_time1:
					if self.note[i] in self.dist_time1[self.note[i-1]]:
						if self.note_type[i] in self.dist_time1[self.note[i-1]][self.note[i]]:
							if self.timelist[i] in self.dist_time1[self.note[i-1]][self.note[i]][self.note_type[i]][0]:
								index = self.dist_time1[self.note[i-1]][self.note[i]][self.note_type[i]][0].index(self.timelist[i])
								self.dist_time1[self.note[i-1]][self.note[i]][self.note_type[i]][1][index] += 1
							else:
								self.dist_time1[self.note[i-1]][self.note[i]][self.note_type[i]][0].append(self.timelist[i])
								self.dist_time1[self.note[i-1]][self.note[i]][self.note_type[i]][1].append(1)
						else:
							self.dist_time1[self.note[i-1]][self.note[i]][self.note_type[i]] = [self.timelist[i]],[1]
					else:
						self.dist_time1[self.note[i-1]][self.note[i]] = {}
						self.dist_time1[self.note[i-1]][self.note[i]][self.note_type[i]] = [self.timelist[i]],[1]
				else:
					self.dist_time1[self.note[i-1]] = {}
					self.dist_time1[self.note[i-1]][self.note[i]] = {}
					self.dist_time1[self.note[i-1]][self.note[i]][self.note_type[i]] = [self.timelist[i]],[1]
		
		for i in range(0,len(self.note)):
			if self.note[i] == -1:
				pass
			else:
				if self.note[i] in self.dist_time2:
					if self.note_type[i] in self.dist_time2[self.note[i]]:
						if self.timelist[i] in self.dist_time2[self.note[i]][self.note_type[i]][0]:
							index = self.dist_time2[self.note[i]][self.note_type[i]][0].index(self.timelist[i])
							self.dist_time2[self.note[i]][self.note_type[i]][1][index] += 1
						else:
							self.dist_time2[self.note[i]][self.note_type[i]][0].append(self.timelist[i])
							self.dist_time2[self.note[i]][self.note_type[i]][1].append(1)
					else:
						self.dist_time2[self.note[i]][self.note_type[i]] = [self.timelist[i]],[1]
				else:
					self.dist_time2[self.note[i]] = {}
					self.dist_time2[self.note[i]][self.note_type[i]] = [self.timelist[i]],[1]
				
			


		# print(self.dist_time)

	def buildXY(self, window_size):
		seq_length = window_size
		for i in range(0, len(self.note) - seq_length, 1):
			if -1 in self.note[i:i+seq_length]:
				pass
			else:
				seq_in = self.note[i:i + seq_length]
				seq_out = self.note[i + seq_length]
				self.dataX.append(seq_in)
				self.dataY.append(seq_out)
			# print (seq_in, '->', seq_out)

		# convert list of lists to array and pad sequences if needed
		X = pad_sequences(self.dataX, maxlen=seq_length, dtype='float32')

		# reshape X to be [samples, time steps, features]
		X = np.reshape(self.dataX, (X.shape[0], seq_length, 1))

		# normalize
		X = X / float(128)

		y = []
		# one hot encode the output variable
		for i in range(0, len(self.dataY)):
			oh_note = [0]*128
			oh_note[self.dataY[i]] = 1
			y.append([oh_note])
		y = np.reshape(y, (len(self.dataY),128))

		return X,y

	def get_dataX(self):
		return self.dataX	

	def get_note_corpus(self):
		return self.note

	def save_data(self):
		with open("note_corpus.pkl", "wb") as fp:   #Pickling
			pickle.dump(self.note, fp)

		with open("dataX.pkl", "wb") as fp:   #Pickling
			pickle.dump(self.dataX, fp)

		with open("dataY.pkl", "wb") as fp:   #Pickling
			pickle.dump(self.dataY, fp)

		with open("dist_time1.pkl", "wb") as fp:   #Pickling
			pickle.dump(self.dist_time1, fp)

		with open("dist_time2.pkl", "wb") as fp:   #Pickling
			pickle.dump(self.dist_time2, fp)

		print("Saved Corpus to disk...")

	def load_dataX(self):
		with open("dataX.pkl", "rb") as fp:   # Unpickling
			data = pickle.load(fp)
		print("Loaded data for start song...")
		return data

	def load_dist_time(self):
		with open("dist_time1.pkl", "rb") as fp:   # Unpickling
			data1 = pickle.load(fp)

		with open("dist_time2.pkl", "rb") as fp:   # Unpickling
			data2 = pickle.load(fp)
		print("Loaded time distribution...")
		return data1, data2

	def get_dist_time(self):
		return self.dist_time

	def print_note_corpus(self):
		print(self.note)

	def print_dist_time(self):
		print(self.dist_time)