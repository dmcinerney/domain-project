#This is the script to run the complete pre-processing pipeline
#this script should be run from the bottom level of the package

#example command line run:
#python domain-project/scripts/querytime_processing.py domain-project/ -q sports

#FIXME: add a file to tell what settings were used

import argparse
import os
import sys
import pandas as pd
import pickle as pkl

def select_titles(titles, labels_file):
	#FIXME: this is a temporary solution (should get a real dev set)
	finaltitles = []
	labels = {}
	with open("domain-project/temp_preprocessing0/dataset.csv", "r") as dataset:
		df = pd.read_csv(dataset)
		for i,row in df.iterrows():
			Xtemps = eval(row[3])
			ytemp = str(row[1])
			for Xtemp in Xtemps:
				finaltitles.append(Xtemp[0])
				labels[Xtemp[0]] = ytemp
	with open(labels_file, "w") as labelsfile:
		pkl.dump(labels, labelsfile)
	return finaltitles


def produce_vectorized_file(file):
	pass

def convert_name(name):#FIXME: why is this necessary, change it
	newname = ""
	for character in name:
		try:
			newname += character.encode()
		except UnicodeEncodeError:
			print("excluding characters")
	return newname

def get_vectors(indices_file, vectors_file, labels_file=None):
	printnum = 10
	print("loading the article vectors")
	import python.Preprocessing.get_article_dataset as get_article_dataset
	vectors_obj = get_article_dataset.load_vectors(indices_file, vectors_file)
	titles = vectors_obj[0].keys()
	titles = select_titles(titles, labels_file)
	names = []
	vectors = []
	labels = None
	if labels_file and os.path.isfile(labels_file):
		with open(labels_file, "r") as labelsfile:
			labels_dict = pkl.load(labelsfile)
		labels = []
	print("compiling dataset")
	for i,title in enumerate(titles[:100]):#FIXME: this is temporary
		vector = get_article_dataset.get_article_vector(title.replace("_"," "), vectors_obj)
		if type(vector) == type(None):
			print("No vector for "+title+" so excluding example from set")
			if (i+1) % printnum == 0:
				print(str(i+1)+" / "+str(len(titles)))
			continue
		names.append(title)
		vectors.append(vector)
		if type(labels) != type(None):
			labels.append(labels_dict[title])
		if (i+1) % printnum == 0:
			print(str(i+1)+" / "+str(len(titles)))
	return names, vectors, labels

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	#FIXME: may want to add "help=" to all of these
	parser.add_argument("path_to_repository")
	parser.add_argument("-q", "--query_term", type=str, default=None)
	parser.add_argument("-a", "--articles_file", type=str, default=None)
	parser.add_argument("-e", "--embeddings_file", type=str, default=None)
	parser.add_argument("-O", "--classifier_option", type=str, default=None)
	parser.add_argument("-S", "--start_from_scratch", action="store_true")

	args = parser.parse_args()

	initial_working_directory = os.getcwd()

	#query-time processing path names
	path_to_repository = os.path.join(initial_working_directory,args.path_to_repository)
	sys.path.append(path_to_repository)#FIXME: there is a lot of commentary on this, not sure if it's the right way to do it
	models_folder = os.path.join(path_to_repository,"models")
	querytime_processing_folder = os.path.join(path_to_repository,"python/QueryTimeProcessing")

	#handling cache folder
	temp_folder = os.path.join(path_to_repository,"temp_querytime0")
	if args.start_from_scratch:
		i = 0
		while os.path.isdir(temp_folder):
			i += 1
			temp_folder = temp_folder[:-len(str(i-1))] + str(i)
		if i >= 5:
			raise Exception("You should clean up your caches! There are already "+str(i)+" of them. No more are allowed. :(")
	if not os.path.isdir(temp_folder):
		os.system("mkdir "+temp_folder)
		print("creating cache \""+temp_folder+"\"")
	else:
		print("defaulting to using \""+temp_folder+"\" as the current cache")

	#query-time processing file names
	classifiers_file = os.path.join(models_folder,"classifiers.pkl")
	if args.classifier_option == "neuralnet":
		neuralnet_file = os.path.join(models_folder,"nueralnet.pkl")
	else:
		neuralnet_file = None
	domainclassifier_file = os.path.join(models_folder,"domain_classifier.pkl")
	dataset_file = os.path.join(temp_folder,"dataset.csv")
	indices_file = os.path.join(temp_folder,"indices.pkl")
	vectors_file = os.path.join(temp_folder,"vectors.npy")
	labels_file = os.path.join(temp_folder,"labels.pkl")
	vectorizer_file = os.path.join(models_folder,"vectorizer.pkl")
	predictions_file = os.path.join(temp_folder,"predictions.csv")
	
	#run query-time processing pipeline
	import python.QueryTimeProcessing.DomainClassifier as domainclassifier
	classifier = domainclassifier.DomainClassifier(classifiers_file, query_term=args.query_term, option=args.classifier_option, embeddings_file=args.embeddings_file, neuralnet_file=neuralnet_file)
	with open(domainclassifier_file, "wb") as classifierfile:
		pkl.dump(classifier, classifierfile)

	if args.articles_file or (os.path.isfile(vectors_file) and os.path.isfile(indices_file)):
		if not (os.path.isfile(vectors_file) and os.path.isfile(indices_file)):
			print("CREATING VECTOR FILE")
			raise NotImplementedError

		names, vectors, labels = get_vectors(indices_file, vectors_file, labels_file=labels_file)
		if labels:
			predictions_orig, predictions, accuracy = classifier.compute_accuracy(vectors, labels)
		else:
			predictions_orig, predictions = classifier.predict(vectors)
			accuracy = None
		names = [convert_name(name) for name in names]
		predictions_orig = [str(prediction) for prediction in predictions_orig]
		predictions_dict = {"names":names, "predictions_for:"+str(classifier.clusters):predictions_orig}
		if type(predictions) != type(None):
			predictions_dict["predictions_for:"+args.query_term] = predictions
		if labels:
			predictions_dict["labels"] = labels
		print(str([(key,len(value)) for key,value in predictions_dict.items()]))
		pd.DataFrame(predictions_dict).to_csv(predictions_file)
		print("done")
