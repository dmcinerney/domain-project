#This is the script to run the complete pre-processing pipeline
#this script should be run from the bottom level of the package

#example command line run:
#python domain-project/scripts/preprocessing.py domain-project/ NOT DONE YET

def check_if_vectorized(csv_file):
	pass

#returns vectorized file's name
def produce_vectorized_file(file):
	pass

def get_vectors(vectors_file):
	pass

if __name__ == '__main__':
	import argparse
	import os
	import sys
	import pandas as pd
	import pickle as pkl
	parser = argparse.ArgumentParser()

	#FIXME: may want to add "help=" to all of these
	parser.add_argument("path_to_repository")
	parser.add_argument("query_term")
	parser.add_argument("-a", "--articles_file", type=str, default=None)
	parser.add_argument("-v", "--vectors_file", type=str, default=None)
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
	classifiertype_file = os.path.join(models_folder,"classifiertype.pkl")
	if args.classifier_option == "neuralnet":
		neuralnet_file = os.path.join(models_folder,"nueralnet.pkl")
	else:
		neuralnet_file = None
	domainclassifier_file = os.path.join(models_folder,"domain_classifier.pkl")
	dataset_file = os.path.join(temp_folder,"dataset.csv")
	indices_file = os.path.join(temp_folder,"indices.pkl")
	vectors_file = os.path.join(temp_folder,"vectors.npy")
	vectorizer_file = os.path.join(models_folder,"vectorizer.pkl")
	
	#run query-time processing pipeline
	import python.QueryTimeProcessing.DomainClassifier as domainclassifier
	with open(classifiertype_file, "rb") as classifiertypefile:
		classifier_type = pkl.load(classifiertypefile)
	if classifier_type[-5:] == "multi":
		allinone = True
	else:
		allinone = False
	classifier = domainclassifier.DomainClassifier(classifiers_file, args.query_term, option=args.classifier_option, neuralnet_file=neuralnet_file, allinone=allinone)
	with open(domainclassifier_file, "wb") as classifierfile:
		pkl.dump(classifier, classifierfile)

	if args.vectors_file or args.articles_file:
		if not args.vectors_file:
			print("CREATING VECTOR FILE")
			if not args.articles_file:
				raise Exception("no articles file!")
			raise NotImplementedError
		else:
			vectors_file = args.vectors_file

		names, vectors, labels = get_vectors(vectors_file)
		if labels:
			predictions, accuracy = classifier.compute_accuracy(vectors, labels)
		else:
			predictions = classifier.get_predictions(vectors)
			accuracy = None
		rows = [(name, prediction) for name, prediction in zip(names, predictions)]
		pd.DataFrame.from_records(rows).to_csv(predictions_file)
