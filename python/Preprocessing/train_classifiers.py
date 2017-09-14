import numpy as np
import pandas as pd
from sklearn.externals import joblib
from sklearn import svm
import random
import os
import pickle as pkl
from sklearn.multiclass import OneVsRestClassifier
from sklearn.multiclass import OneVsOneClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.neighbors import KNeighborsClassifier

#multi types are < 0 and binary types are >= 0
_classifier_types = {"knn_multi":-1,"svm_binary":0}

'''
def get_data(dataset_file):
	with open(dataset_file, "r") as dataset:
		print("reading csv file ("+dataset_file+")")
		df = pd.read_csv(dataset)
		#y, X = zip(*[(row[0],eval(row[1])) for i,row in df.iterrows()])
		#list of tuples
		Xy = []
		names_dict = {}
		for i,row in df.iterrows():
			ytemp = str(row[1])
			nametemp = row[2]
			Xtemps = eval(row[3])
			Xy.extend([(Xtemp[1], ytemp) for Xtemp in Xtemps if type(Xtemp[1]) != type(None)])
			names_dict[ytemp] = nametemp
			if (i+1)%1 == 0:
				print(str(i+1)+" / "+str(df.shape[0]))
		np.random.shuffle(Xy)
		X, y = zip(*Xy)
	return X, y, names_dict
'''

def get_data(dataset_file):
	with open(dataset_file, "r") as dataset:
		print("reading csv file ("+dataset_file+")")
		df = pd.read_csv(dataset)
		names = []
		X = []
		y = []
		for i,row in df.iterrows():
			article = eval(row[1])
			names.append(article[0])
			X.append(article[1])
			y.append(row[2])
			if (i+1)%10000 == 0 or i+1 == df.shape[0]:
				print(str(i+1)+" / "+str(df.shape[0]))
	return X, y, names

def main(clusternames_file, dataset_file, classifiers_file, classifier_type):

	if classifier_type in _classifier_types.keys():
		type_id = _classifier_types[classifier_type]
	else:
		raise Exception("No classifier by the name of "+classifier_type+" is available!")

	X,y, names = get_data(dataset_file)

	if type_id >= 0:
		clusterids = []
		classifiers = []
		for clusterid in list(set(y)):
			if type_id == 0:
				clf = svm.SVC()
			ytemp = []
			for label in y:
				if clusterid == label:
					ytemp.append(1)
				else:
					ytemp.append(0)
			clf.fit(X,ytemp)
			clusterids.append(clusterid)
			classifiers.append(clf)
	else:
		mlb = MultiLabelBinarizer()
		ytemp = mlb.fit_transform(y)
		clusterids = list(mlb.classes_)

		if type_id == -1:
			classifiers = OneVsRestClassifier(KNeighborsClassifier()).fit(X,ytemp)

	with open(clusternames_file, "rb") as clusternamesfile:
		clusternamesdict = dict(pkl.load(clusternamesfile))
	clusternames = [clusternamesdict[clusterid] for clusterid in clusterids]

	clftuple = (classifier_type,clusterids,clusternames,classifiers)

	with open(classifiers_file, "wb") as classifiersfile:
		pkl.dump(clftuple, classifiersfile)


if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("clusternames_file")
	parser.add_argument("dataset_file")
	parser.add_argument("classifiers_file")
	parser.add_argument("classifier_type", help="The following are the possible options for different classifiers: "+str(_classifier_types.keys()))

	args = parser.parse_args()

	#the allinone option is to train one multi-class classifier
	main(args.clusternames_file,args.dataset_file,args.classifiers_file,args.classifier_type)
