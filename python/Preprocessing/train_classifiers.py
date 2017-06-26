import pandas as pd

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("dataset_file")
	parser.add_argument("-c", "--classifier_type", type=str, default="svm")
	parser.add_argument("-p", "--preprocessing_method", type=str, default="lda")

	args = parser.parse_args()

	with open(dataset_file, "r") as dataset:
		print("reading csv file ("+dataset_file+")")
		df = pd.read_csv(dataset)
