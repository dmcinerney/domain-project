import pickle

class DomainClassifier:
	def __init__(self, classifiers_file, query_term, option="cosine_sim", neuralnet_file=None):
		self.option = option
		self.query_term = query_term
		if neuralnet_file:
			if option != "neuralnet":
				print("Warning: no need to give neural network file because it is not being used.  (Set option to \"neuralnet\" if you would like to use it.)")
			else:
				self.neuralnet_file = neuralnet_file
		with open(classifiers_file, "rb") as classifiersfile:
			self.classifiers = pickle.loads(classifiersfile)
		print("Making classifier from "+str(len(self.classifiers))+" subclassifiers")

	def predict(self, vector):
		predictions = [(clusterid,name,clf.predict(vector)) for clusterid,name,clf in self.classifiers]

		final_prediction = None

		if self.option == "cosine_sim":
			raise NotImplementedError
		elif self.option == "neuralnet":
			raise NotImplementedError
		else:
			raise Exception("No option by the name \""+self.option+"\"")

		return final_prediction

	def get_predictions(self, vectors):
		return [self.predict(vector) for vector in vectors]

	def compute_accuracy(self, vectors, labels):
		predictions = self.get_predictions(vectors)
		correct = 0
		for i,prediction in enumerate(predictions):
			if labels[i] == prediction:
				correct += 1
		accuracy = float(correct)/len(predictions)
		return predictions, accuracy
		