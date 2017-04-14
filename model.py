import numpy as np
import os
import h5py
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.utils import np_utils
# fix random seed for reproducibility

lowerBound = 24
upperBound = 102
np.random.seed(7)

class Model(object):
	"""docstring for Model"""
	def __init__(self):
		super(Model, self).__init__()
		# self.note_sheet = note_sheet
		self.seq_length = 1
		self.X = []
		self.y = []
		self.batch_size = 1
		self.epoch = 1
		# self.cycle = 1
		self.model = Sequential()
		# self.loss = 'mean_squared_error'
		self.loss = 'binary_crossentropy'
		# self.loss = 'categorical_crossentropy'
		# self.loss = 'mean_absolute_error'
		
	def init_data(self):
		self.X = np.array([[0]*(upperBound-lowerBound)]*16)
		self.y = [[0]*(upperBound-lowerBound)]
		return self.y

	def make_data(self, Y):
		self.X = np.reshape(self.X, (16,1,78))
		self.y = np.reshape(Y, (1,1,78))
		# print (len(self.X), len(self.y))
		# for x in self.X:
		# 	print ("X: " ,x)
		# 	print ("Y: " ,self.y)

	def slide_window(self):
		self.X = np.append(self.X, self.y, axis=0)
		self.X = np.delete(self.X,0,0)

	def create_model(self):
		self.model.add(LSTM(78, batch_input_shape=(self.batch_size, 1, 78), stateful=True, return_sequences = True))
		self.model.add(LSTM(78, activation='softmax', return_sequences = True))
		self.model.compile(loss=self.loss, optimizer='adam', metrics=['accuracy'])

	def fit_model(self):
		for i in range(0, 16):
			x = np.reshape(self.X[i], (1,1,78))
			# print(x)
			# print("Cycle: {}/{}".format(i+1, self.cycle))
			self.model.fit(x, self.y, nb_epoch=self.epoch, batch_size=self.batch_size, verbose=2, shuffle=False)
		self.model.reset_states()

	def summarize(self):
		# TODO make test data to X self.X should be (1,1,78)
		scores = self.model.evaluate(self.X, self.y, batch_size=self.batch_size, verbose=0)
		self.model.reset_states()
		print("Model Accuracy: %.2f%%" % (scores[1]*100))
		return self.model

	def save_model(self):
		# serialize model to JSON
		model_json = self.model.to_json()
		with open("./model/model.json", "w") as json_file:
		    json_file.write(model_json)
		# serialize weights to HDF5
		self.model.save_weights("./model/model.h5")
		print("Saved model to disk")

	def load_model(self):
		# load json and create model
		json_file = open('./model/model.json', 'r')
		loaded_model_json = json_file.read()
		json_file.close()
		loaded_model = model_from_json(loaded_model_json)
		# load weights into new model
		loaded_model.load_weights("./model/model.h5")
		print("Loaded model from disk")
