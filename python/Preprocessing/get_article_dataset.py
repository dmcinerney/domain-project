import make_wiki_adjacencies
import graph_manip
import pandas as pd
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

def get_article_vectors(title, vector_file):
	#tar -zxvf <tar filename> <file you want to extract> ?
	#NEED TO IMPLEMENT
	#use concrete
	#or use pre-trained vectors (like lda vectors) for each document
	pass

def get_cluster_articles(G, categories, vector_file):
	articles = []
	for category in categories:
		if category in G.nodes():
			for neighbor in G.neighbors(category):
				if not neighbor[:9] == "Category:":
					articles.append((neighbor,get_article_vectors(neighbor, vector_file)))
	return articles

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("article_categories_file")
	parser.add_argument("adjacencies_file")
	parser.add_argument("cluster_groupings_file")
	parser.add_argument("cluster_names_file")
	parser.add_argument("vector_file")
	parser.add_argument("dataset_file")

	args = parser.parse_args()

	article_categories_file = args.article_categories_file
	adjacencies_file = args.adjacencies_file
	cluster_names_file = args.cluster_names_file
	cluster_groupings_file = args.cluster_groupings_file
	vector_file = args.vector_file
	dataset_file = args.dataset_file

	#attach articles to category graph
	G = graph_manip.DiGraph()
	make_wiki_adjacencies.add_adjacencies(G, article_categories_file)

	#get cluster_names, cluster_categories from cluster_names_file and cluster_groupings_file
	cluster_names = get_cluster_names(cluster_names_file)
	cluster_categories = get_cluster_categories(cluster_groupings_file)

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
		articles = get_cluster_articles(G,cluster_categories[cluster_id], vector_file)
		rows.append(cluster_id,cluster_name,articles)
		if ((i+1) % 1) == 0:
			print(str(i+1)+" / "+str(len(cluster_names)))
	pd.DataFrame.from_records(rows).to_csv(dataset_file)
