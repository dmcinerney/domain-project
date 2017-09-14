import make_wiki_adjacencies
import graph_manip
import pandas as pd
import numpy as np
import pickle as pkl
#import concrete

def get_cluster_categories(cluster_groupings_file):
	'''
	cluster_groupings = {}
	with open(cluster_groupings_file, 'r') as clustergroups:
		for line in clustergroups:
			line = line.strip()
			splitline = line.split()
			cluster_id = " ".join(splitline[:2])
			cluster_grouping = eval(line[len(cluster_id)+1:])
			cluster_groupings[cluster_id] = cluster_grouping
	return cluster_groupings
	'''
	with open(cluster_groupings_file, 'r') as clustergroups:
		return pkl.load(clustergroups)

def load_vectors(index_file,vector_file):
	with open(index_file, "r") as title_to_index:
		indices = pkl.load(title_to_index)

	vectors = np.load(vector_file)

	return (indices, vectors)

def convert_title(title):
	#FIXME: something weird going on with binary characters? u'\x81'? just converting it to string and hoping it's ok for now
	'''
	newtitle = ""
	for character in title:
		newtitle += chr(ord(character))
	return newtitle.replace("_"," ")
	'''
	return title

def get_article_vector(title, vectors_obj):
	indices = vectors_obj[0]
	vectors = vectors_obj[1]
	key = convert_title(title)
	if key in indices.keys():
		return vectors[indices[convert_title(title)]].tolist()
	else:
		return None

def get_cluster_articles(G, categories, vectors_obj):
	articles = []
	for category in categories:
		if category in G.nodes():
			for neighbor in G.neighbors(category):
				if neighbor[:9] != "Category:":
					vector = get_article_vector(neighbor, vectors_obj)
					'''
					if type(vector) != type(None):
						articles.append((neighbor,vector))
					'''
					articles.append((neighbor,vector))
	return articles

def partition_dataset(rows, fraction_dev):
	if type(rows) == str:
		with open(rows, "r") as rowsfile:
			df = pd.read_csv(dataset)
			rows = [[row[1],row[2]] for i,row in df.iterrows()]
	np.random.shuffle(rows)
	#separate into train and test
	numdev = int(len(rows)*fraction_dev)
	dev_rows = rows[:numdev]
	train_rows = rows[numdev:]

	return train_rows, dev_rows

def main(article_categories_file,cluster_groupings_file,index_file,vector_file,dataset_file,fraction_dev):
	#attach articles to category graph
	G = graph_manip.DiGraph()
	make_wiki_adjacencies.add_adjacencies(G, article_categories_file)

	#get cluster_names, cluster_categories from cluster_groupings_file
	clusters_categories = get_cluster_categories(cluster_groupings_file)

	vectors_obj = load_vectors(index_file, vector_file)

	rows = []

	#NO LONGER IN USE: For each category in each cluster, write out article titles and vectors in that category to file (grouped by cluster)
	#write out article titles and vectors and labels sorted randomly and separated into dev and training set
	for i,(cluster_id,cluster_categories) in enumerate(clusters_categories.items()):
		#if i > 44: break
		articles = get_cluster_articles(G,cluster_categories, vectors_obj)
		for article in articles:
			rows.append((str(article),cluster_id))
		#rows.append((cluster_id,cluster_name,articles))
		if ((i+1) % 1) == 0:
			print("there are "+str(len(articles))+" articles in cluster "+str(i))
			print(str(i+1)+" / "+str(len(clusters_categories)))
	
	np.random.shuffle(rows)
	#pd.DataFrame.from_records(rows).to_csv(dataset_file) # do we ever need the combined train and dev? no

	train_rows, dev_rows = partition_dataset(rows, fraction_dev)

	pd.DataFrame.from_records(train_rows).to_csv(dataset_file[:-4]+"_train.csv")
	pd.DataFrame.from_records(dev_rows).to_csv(dataset_file[:-4]+"_dev.csv")


if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("article_categories_file")
	parser.add_argument("cluster_groupings_file")
	parser.add_argument("index_file")
	parser.add_argument("vector_file")
	parser.add_argument("dataset_file")

	args = parser.parse_args()

	main(args.article_categories_file,args.cluster_groupings_file,args.index_file,args.vector_file,args.dataset_file)
