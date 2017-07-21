import numpy as np
import pickle as pkl

def top_category(prediction):
	return max(enumerate(prediction), key=lambda x: x[1])[0]


class DomainClassifier:
	options = ["cosine_sim", "neuralnet"]
	def __init__(self, classifiers_file, query_term=None, option=None, neuralnet_file=None, embeddings_file=None):
		with open(classifiers_file, "rb") as classifiersfile:
			(self.clftype,ids,names,self.classifiers) = pkl.load(classifiersfile)
			self.clusters = zip(ids,names)
		if type(self.classifiers) == list:
			print("Making classifier from "+str(len(self.clusters))+" "+self.clftype+" subclassifiers")
		else:
			print("Making classifier from one "+str(len(self.clusters))+"-class "+self.clftype+" classifier")

		self.query_term = query_term
		self.option = option

		if self.query_term:
			if self.option not in self.options:
				raise Exception("No option specified for producing binary classification for domain term!")
			else:
				if embeddings_file or self.option == "cosine_sim":
					if self.option != "cosine_sim":
						print("Warning: no need to give embeddings file because it is not being used.  (Set option to \"cosine_sim\" if you would like to use it.)")
					else:
						self.weights = []
						import python.Preprocessing.make_wiki_adjacencies as make_wiki_adjacencies
						embeddings = make_wiki_adjacencies.get_embeddings(embeddings_file)
						domain_rep = make_wiki_adjacencies.get_embedding_rep(query_term.split(), embeddings)
						for cluster_id,cluster_name in self.clusters:
							embedding_rep = make_wiki_adjacencies.get_embedding_rep(cluster_name[9:].split(), embeddings) #FIXME: there could be a different way to come up with embeddings for cluster names
							self.weights.append(make_wiki_adjacencies.get_cosine_sim(domain_rep,embedding_rep))
						self.weights = np.divide(self.weights,sum(weights))
				if neuralnet_file or self.option == "neuralnet":
					if self.option != "neuralnet":
						print("Warning: no need to give neural network file because it is not being used.  (Set option to \"neuralnet\" if you would like to use it.)")
					else:
						raise NotImplementedError

	def predict(self, vectors, returnboth=False):
		print("getting predictions")
		if type(self.classifiers) != list:
			#contains lists of predictions for each predictor
			predictions = self.classifiers.predict(vectors)
		else:
			#contains lists of predictions for each predictor
			predictions = [clf.predict(vectors) for clf in self.classifiers]


		if self.query_term == None or self.option == None:
			if returnboth:
				raise Exception("Can't return both if query term is None!")
			print("done getting predctions")
			return predictions

		#contains list of binary predictions of in domain or not
		final_predictions = None

		#algorithmically determines weights on each prediction via cosine similarity between domain term and cluster terms
		if self.option == "cosine_sim":
			final_predictions = [np.dot(self.weights, prediction) for prediction in predictions]
		#uses neural network to predict with domain term's vector and "prediction space" rep of article
		elif self.option == "neuralnet":
			raise NotImplementedError
		else:
			raise Exception("No option by the name \""+self.option+"\"")

		print("done getting predctions")
		if returnboth:
			return predictions, final_predicitons
		else:
			return final_predictions


	def compute_accuracy(self, vectors, labels):
		predictions = self.predict(vectors)
		print("computing accuracy")
		correct = 0
		for i,prediction in enumerate(predictions):
			if self.query_term == None:#then label and prediction are each lists
				if top_category(labels[i]) == top_category(prediction):
					correct += 1
			else:#label and prediction are each a boolean value
				if labels[i] == top_category:
					correct += 1
		accuracy = float(correct)/len(predictions)
		print("accuracy: "+str(accuracy))
		return predictions, accuracy

