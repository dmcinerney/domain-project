import pickle

class DomainClassifier:
	def __init__(self, classifiers_file, query_term, option="cosine_sim", neuralnet_file=None, allinone=False):
		self.option = option
		self.query_term = query_term
		self.allinone = allinone
		if neuralnet_file:
			if option != "neuralnet":
				print("Warning: no need to give neural network file because it is not being used.  (Set option to \"neuralnet\" if you would like to use it.)")
			else:
				self.neuralnet_file = neuralnet_file
		with open(classifiers_file, "rb") as classifiersfile:
			self.classifiers = pickle.load(classifiersfile)
		if not self.allinone:
			print("Making classifier from "+str(len(self.classifiers))+" subclassifiers")
		else:
			pass

	def predict(self, vector):
		if self.allinone:
			predictions = self.classifiers.predict(vector)
			#need to convert to multiclass labels
			raise NotImplementedError
		else:
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
		
