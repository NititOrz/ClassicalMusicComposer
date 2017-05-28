import numpy as np
from keras.preprocessing.sequence import pad_sequences

class Predictor(object):
	"""docstring for Predictor"""
	def __init__(self, model):
		self.model = model
		self.note_list = []

	def predict_on_corpus(self, dataX, seq_length):
		# print(dataX)
		pattern_index = np.random.randint(len(dataX))
		# print(pattern_index)
		pattern = dataX[pattern_index]
		self.note_list = np.copy(pattern)
		for i in range(600):
			x = pad_sequences([pattern], maxlen=seq_length, dtype='float32')
			x = np.reshape(x, (1, seq_length, 1))
			x = x / float(128)
			prediction = self.model.predict(x, verbose=0)
			# index = np.argmax(prediction)
			index = prediction[0].argsort()[-2:][::-1]
			# print (pattern, "->", index)
			# new_note = [np.random.choice(index)]
			new_note = [index[0]]
			self.note_list = np.append(self.note_list, np.copy(new_note), axis=0)
			pattern = np.append(pattern, np.copy(new_note), axis=0)
			pattern = np.delete(pattern,0,0)
		
	def buildNotetype(self):
		note_and_type_list = []
		type_checker = np.array([0]*128)
		for n in self.note_list:
			type_checker[n] += 1
			type_checker = type_checker%2
			if type_checker[n] == 1:
				note_and_type_list.append((1, n))
			else:
				note_and_type_list.append((0, n))

		return note_and_type_list

	def buildSong(self, note_and_type, dist_time1, dist_time2):
		print("Building Song.....")
		song = []
		checker = []
		for i in range(1,len(note_and_type)):
			try:
				# print(dist_time[note_and_type[i-1][1]][note_and_type[i][1]][note_and_type[i][0]])
				temp = dist_time1[note_and_type[i-1][1]][note_and_type[i][1]][note_and_type[i][0]]
				print(temp)
			except:
				try:
					# print(note_and_type[i][0])
					temp = dist_time2[note_and_type[i][1]][note_and_type[i][0]]

				except:
					# print(note_and_type[i][1])
					temp = ([128, 256],[1,9])
					# temp = ([128,256,512],[1,4,1])
					checker.append(1)

			# temp = dist_time[note_and_type[i-1][1]][note_and_type[i][1]][note_and_type[i][0]]
			list_of_candidates = temp[0]
			probability_distribution = np.array(temp[1])
			probability_distribution = np.array(temp[1])/sum(temp[1])
			number_of_items_to_pick = 1
			time = np.random.choice(list_of_candidates, number_of_items_to_pick, p=probability_distribution)
			if note_and_type[i][0] == 1:
				note_type = "note_on"
			else:
				note_type = "note_off"
			song.append((note_type, note_and_type[i][1], time[0]))
		# print(len(checker))
		return song

	def get_note_list(self):
		return self.note_list

	def print_note_list(self):
		print(self.note_list)