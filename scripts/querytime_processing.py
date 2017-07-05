#This is the script to run the complete pre-processing pipeline
#this script should be run from the bottom level of the package

#example command line run:
#python domain-project/scripts/preprocessing.py domain-project/ NOT DONE YET

def check_if_vectorized(csv_file):
	pass

#returns vectorized file's name
def produce_vectorized_file(file):
	pass

if __name__ == '__main__':
	import argparse
	import os
	import python.QueryTimeProcessing.DomainClassifier as domainclassifier
	import pandas as pd
	parser = argparse.ArgumentParser()

	#FIXME: may want to add "help=" to all of these
	parser.add_argument("path_to_repository")
	parser.add_argument("query_term")
	parser.add_argument("-a", "--articles_file", type=str, default=None)
	parser.add_argument("-v", "--vectors_file", type=str, default=None)
	parser.add_argument("-o", "--classifier_option", type=str, default=None)
	parser.add_argument("-s", "--start_from_scratch", action="store_true")
	parser.add_argument("-e", "--erase_temp", action="store_true")

	args = parser.parse_args()

	initial_working_directory = os.getcwd()
	os.chdir(args.path_to_repository)

	#query-time processing path names
	models_folder = "models"
	preprocessing_folder = "python/QueryTimeProcessing"
	temp_folder = "temp_querytime"

	#query-time processing file names
	vectors_file = os.path.join(temp_folder,"vectors.csv")
	classifiers_file = os.path.join(models_folder,"classifiers.pkl")
	if classifier_option == "neuralnet":
		neuralnet_file = os.path.join(models_folder,"nueralnet.pkl")
	else:
		neuralnet_file = None
	domainclassifier_file = os.path.join(models_folder,"domain_classifier.pkl")
	vectors_file = os.path.join(temp_folder,"vectors.csv") #FIXME: not sure what type of file this should be (same format as whatever Zhenya gives me maybe)
	predictions_file = "predictions.csv"

	args = parser.parse_args()
	if args.start_from_scratch:
		os.system("rm -r "+temp_folder)
	if not os.path.isdir(temp_folder):
		os.system("mkdir "+temp_folder)

	#run query-time processing pipeline
	classifier = domainclassifier.DomainClassifier(classifiers_file, args.query_term, option=args.classifier_option, neuralnet_file=neuralnet_file)
	with open(domainclassifier_file, "wb") as classifierfile:
		classifierfile.write(pickle.dumps(classifier))

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

	if args.erase_temp:
		os.system("rm -r "+temp_folder)

	os.chdir(initial_working_directory)
