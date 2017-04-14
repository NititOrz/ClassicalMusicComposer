import numpy as np

class Predictor(object):
	"""docstring for Predictor"""
	def __init__(self, model):
		self.model = model
		self.treshold = 0.25

	def estimate(self, pred):
		for i in range(0,len(pred)):
			for j in range(0,len(pred[i])):
				if pred[i][j] > (0.5 + self.treshold):
					pred[i][j] = 1
				elif pred[i][j] < (0.5 - self.treshold):
					pred[i][j] = -1
				else:
					pred[i][j] = 0
		return pred


	def predict(self):
		seed = np.array([0]*82)
		for i in range(0,1):
			x = np.reshape(seed, (1,1,82))
			prediction = self.model.predict(x, verbose=0)
			# prediction = self.estimate(prediction)
			print(prediction)
			seed = np.array(prediction)
		# index = np.argsort(prediction)
		# print (int_to_char[seed[0]], "->", int_to_char[index])
		# seed = 
		# for i in index:
		# 	print(prediction[i])
		# print(index[:][-4:])
		self.model.reset_states()
		