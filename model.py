import numpy as np
import os
import h5py
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.utils import np_utils
from keras.models import model_from_json
from keras.callbacks import ModelCheckpoint
# fix random seed for reproducibility

class Model(object):
	"""docstring for Model"""
	def __init__(self):
		self.model = Sequential()
		self.batch_size = 256
	
	def createModel(self, X, y):	
		print("Creating Model.....")
		# self.batch_size = X.shape[0]
		self.model.add(LSTM(128, input_shape=(X.shape[1], X.shape[2])))
		# self.model.add(LSTM(64, input_shape=(X.shape[1], X.shape[2])))
		self.model.add(Dense(y.shape[1], activation='softmax'))
		# self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
		print("Done!")

	def compileModel(self):
		print("Compiling Model.....")
		self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
		print("Done!!")

	def trainModel(self, X, y):
		print("Training Model.....")
		filepath="./model/weights-improvement-{epoch:03d}-{loss:.4f}.hdf5"
		checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=0, save_best_only=True, mode='min')
		callbacks_list = [checkpoint]
		self.model.fit(X, y, epochs=1, batch_size=self.batch_size, verbose=1, callbacks = callbacks_list)
		print("Done!!!")

	def testModel(self, X, y):
		# summarize performance of the 
		print("Testing Model.....")
		scores = self.model.evaluate(X, y, verbose=0)
		print("Model Accuracy: %.2f%%" % (scores[1]*100))

	def save_model(self):
		# serialize model to JSON
		print("Saving Model.....")
		model_json = self.model.to_json()
		with open("./model/model.json", "w") as json_file:
		    json_file.write(model_json)
		# serialize weights to HDF5
		self.model.save_weights("./model/model.h5")
		print("Saved model to disk")

	def load_model(self, model, weights):
		# load json and create model
		print("Loading Model.....")
		json_file = open(model, 'r')
		loaded_model_json = json_file.read()
		# print(loaded_model_json)
		loaded_model = model_from_json(loaded_model_json)
		json_file.close()
		# load weights into new model
		loaded_model.load_weights(weights)
		print("Loaded model from disk")
		self.model = loaded_model

	def get_model(self):
		return self.model