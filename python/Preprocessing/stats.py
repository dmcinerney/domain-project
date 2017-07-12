#script gets stats about wikipedia and the clusters
import train_classifiers
import numpy as np
import pandas as pd

def get_data(dataset_file):
	with open(dataset_file, "r") as dataset:
		print("reading csv file ("+dataset_file+")")
		df = pd.read_csv(dataset)
		clusters = []
		for i,row in df.iterrows():
			ytemp = row[1]
			nametemp = row[2]
			Xtemps = eval(row[3])
			clusters.append((ytemp,nametemp,Xtemps))
			if (i+1)%1 == 0:
				print(str(i+1)+" / "+str(df.shape[0]))
	return clusters

def get_vectors(listobj):
	vectorlist = [a[1] for a in listobj if type(a[1]) != type(None)]
	return vectorlist

def main(dataset_file,stats_file):
	clusters = get_data(dataset_file)
	ids = []
	names = []
	means = []
	standard_deviations = []
	allvectors = []
	for cluster in clusters:
#		import pdb; pdb.set_trace()
		vectors = get_vectors(cluster[2])
		allvectors.extend(vectors)
		mean = np.mean(vectors, axis=0)
		stdev = np.linalg.norm(np.std(vectors, axis=0))
		ids.append(cluster[0])
		names.append(cluster[1])
		means.append(mean)
		standard_deviations.append(stdev)
		print(cluster[1]+": stdev is "+str(stdev))
	ids.append("TOTAL")
	names.append("TOTAL")
	means.append(np.mean(allvectors))
	standard_deviations.append(np.linalg.norm(np.std(allvectors, axis=0)))
	print("TOTAL stdev is "+str(standard_deviations[-1]))
	pd.DataFrame({"id":ids,"name":names,"standard_deviations":standard_deviations,"mean":means}).to_csv(stats_file)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("dataset_file")
	parser.add_argument("stats_file")

	args = parser.parse_args()

	main(args.dataset_file,args.stats_file)
