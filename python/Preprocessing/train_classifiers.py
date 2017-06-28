import pandas as pd
from sklearn.externals import joblib
from sklearn import svm
import random
import os
import pickle

def get_data(dataset_file):
	with open(dataset_file, "r") as dataset:
		print("reading csv file ("+dataset_file+")")
		df = pd.read_csv(dataset)
		#y, X = zip(*[(row[0],eval(row[1])) for i,row in df.iterrows()])
		#list of tuples
		Xy = []
		names_dict = {}
		for i,row in df.iterrows():
			ytemp = row[0]
			nametemp = row[1]
			Xtemps = eval(row[2])
			Xy.extend([(Xtemp, ytemp)for Xtemp in Xtemps])
			names_dict[ytemp] = namestemp
		np.random.shuffle(Xy)
		X, y = zip(*Xy)
	return X, y, names_dict

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("dataset_file")
	parser.add_argument("classifiers_file")
	parser.add_argument("-c", "--classifier_type", type=str, default="svm")

	args = parser.parse_args()

	X,y,names_dict = get_data(args.dataset_file)
	clusterids = list(set(y))
	classifiers = []

	for clusterid in clusterids:
		if args.classifier_type == "svm":
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
	with open(args.classifiers_file, "wb") as classifiersfile:
		classifiersfile.write(pickle.dumps(classifiers))

'''

>>> clf2 = pickle.loads(s)
'''
