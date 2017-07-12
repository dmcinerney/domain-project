import numpy as np
import pandas as pd
from sklearn.externals import joblib
from sklearn import svm
import random
import os
import pickle as pkl

def get_data(dataset_file):
	with open(dataset_file, "r") as dataset:
		print("reading csv file ("+dataset_file+")")
		df = pd.read_csv(dataset)
		#y, X = zip(*[(row[0],eval(row[1])) for i,row in df.iterrows()])
		#list of tuples
		Xy = []
		names_dict = {}
		for i,row in df.iterrows():
			ytemp = row[1]
			nametemp = row[2]
			Xtemps = eval(row[3])
			Xy.extend([(Xtemp[1], ytemp) for Xtemp in Xtemps if type(Xtemp[1]) != type(None)])
			names_dict[ytemp] = nametemp
			if (i+1)%1 == 0:
				print(str(i+1)+" / "+str(df.shape[0]))
		np.random.shuffle(Xy)
		X, y = zip(*Xy)
	return X, y, names_dict

def main(dataset_file, classifiers_file, classifier_type="svm"):
	X,y,names_dict = get_data(dataset_file)
	clusterids = list(set(y))
	classifiers = []

	for clusterid in clusterids:
		if classifier_type == "svm":
			clf = svm.SVC()
		else:
			raise Exception("No classifier by that name is available!")
		ytemp = []
		for label in y:
			if clusterid == label:
				ytemp.append(1)
			else:
				ytemp.append(0)
		clf.fit(X,ytemp)
		classifiers.append(clusterid,names_dict[clusterid],clf)

	#POSSIBLE: could use joblib, but probably not a good idea
	with open(classifiers_file, "wb") as classifiersfile:
		pkl.dumps(classifiers, classifiersfile)


if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("dataset_file")
	parser.add_argument("classifiers_file")
	parser.add_argument("-c", "--classifier_type", type=str, default="svm")

	args = parser.parse_args()

	main(args.dataset_file, args.classifiers_file, classifier_type=args.classifier_type)
