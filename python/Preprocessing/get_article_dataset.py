import make_wiki_adjacencies
import graph_manip
import pandas as pd
import numpy as np
import pickle as pkl
#import concrete

def get_cluster_names(cluster_names_file):
	cluster_names = []
	with open(cluster_names_file, 'r') as clusternames:
		for line in clusternames:
			splitline = line.strip().split()
			cluster_id = " ".join(splitline[:2])
			cluster_name = splitline[-1]
			cluster_names.append((cluster_id,cluster_name))
	return cluster_names

def get_cluster_categories(cluster_groupings_file):
	cluster_groupings = {}
	with open(cluster_groupings_file, 'r') as clustergroups:
		for line in clustergroups:
			line = line.strip()
			splitline = line.split()
			cluster_id = " ".join(splitline[:2])
			cluster_grouping = eval(line[len(cluster_id)+1:])
			cluster_groupings[cluster_id] = cluster_grouping
	return cluster_groupings

def load_vectors(index_file,vector_file):
	with open(index_file, "r") as title_to_index:
		indecies = pkl.load(title_to_index)

	vectors = np.load(vector_file)

	return (indecies, vectors)

def convert_title(title):
	return title.replace("_"," ")

def get_article_vector(title, vectors_obj):
	indecies = vectors_obj[0]
	vectors = vectors_obj[1]
	return vectors[indecies[convert_title(title)]]

def get_cluster_articles(G, categories, vectors_obj):
	articles = []
	for category in categories:
		if category in G.nodes():
			for neighbor in G.neighbors(category):
				if not (neighbor[:9] == "Category:"):
					articles.append((neighbor,get_article_vectors(neighbor, vectors_obj)))
	return articles

def main(article_categories_file,adjacencies_file,cluster_groupings_file,cluster_names_file,index_file,vector_file,dataset_file):
	#attach articles to category graph
	G = graph_manip.DiGraph()
	make_wiki_adjacencies.add_adjacencies(G, article_categories_file)

	#get cluster_names, cluster_categories from cluster_names_file and cluster_groupings_file
	cluster_names = get_cluster_names(cluster_names_file)
	cluster_categories = get_cluster_categories(cluster_groupings_file)

	vectors_obj = load_vectors(index_file, vector_file)

	#For each category in each cluster, write out articles (from concrete) in that category to file (grouped by cluster)
	'''
	with open(dataset_file, "w") as datafile:
		rows = []
		for i,(cluster_id,cluster_name) in enumerate(cluster_names):
			articles = get_cluster_articles(G,cluster_categories[cluster_id])
			datafile.write(cluster_id+" "+cluster_name+" "+str(articles)+"\n")
			if ((i+1) % 1) == 0:
				print(str(i+1)+" / "+str(len(cluster_names)))
	'''
	rows = []
	for i,(cluster_id,cluster_name) in enumerate(cluster_names):
		#if i > 44: break
		articles = get_cluster_articles(G,cluster_categories[cluster_id], vectors_obj)
		rows.append((cluster_id,cluster_name,articles))
		if ((i+1) % 1) == 0:
			print(str(i+1)+" / "+str(len(cluster_names)))
	pd.DataFrame.from_records(rows).to_csv(dataset_file)


if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("article_categories_file")
	parser.add_argument("adjacencies_file")
	parser.add_argument("cluster_groupings_file")
	parser.add_argument("cluster_names_file")
	parser.add_argument("index_file")
	parser.add_argument("vector_file")
	parser.add_argument("dataset_file")

	args = parser.parse_args()

	main(args.article_categories_file,args.adjacencies_file,args.cluster_groupings_file,args.cluster_names_file,args.index_file,args.vector_file,args.dataset_file)
