import pickle

class DomainClassifier:
	def __init__(self, classifiers_file, query_term, option="cosine_sim"):
		self.option = option
		with open(classifiers_file, "rb") as classifiersfile:
			self.classifiers = pickle.loads(classifiersfile)
		print("Making classifier from "+str(len(self.classifiers))+" subclassifiers")

	def predict(self, vector):
		predictions = [(clusterid,name,clf.predict(vector)) for clusterid,name,clf in self.classifiers]

		if self.option == "cosine_sim":
			raise NotImplementedError
		elif self.option == "neuralnet":
			raise NotImplementedError
		else:
			raise Exception("No option by the name \""+self.option+"\"")