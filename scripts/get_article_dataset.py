import make_wiki_adjacencies
import graph_manip
import concrete

def get_cluster_names(cluster_names_file):
	#NEED TO IMPLEMENT
	pass

def get_cluster_categories(cluster_groupings_file):
	#NEED TO IMPLEMENT
	pass

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()

	parser.add_argument("article_categories_file")
	parser.add_argument("adjacencies_file")
	parser.add_argument("cluster_groupings_file")
	parser.add_argument("cluster_names_file")

	args = parser.parse_args()

	article_categories_file = args.article_categories_file
	adjacencies_file = args.adjacencies_file
	cluster_names_file = args.cluster_names_file
	cluster_groupings_file = args.cluster_groupings_file

	#attach articles to category graph
	G = graph_manip.DiGraph()
	make_wiki_adjacencies.add_adjacencies(G)

	#get cluster_names, cluster_categories from cluster_names_file and cluster_groupings_file
	cluster_names = get_cluster_names(cluster_names_file)
	cluster_categories = get_cluster_categories(cluster_groupings_file)

	#For each category in each cluster, write out articles (from concrete) in that category to file (grouped by cluster)
	for cluster_id,cluster_name in cluster_names:

