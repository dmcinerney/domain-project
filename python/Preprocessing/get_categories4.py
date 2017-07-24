import graph_manip
import make_wiki_adjacencies

def main(input_file,cluster_groupings_file,cluster_names_file,from_dbpedia=False):
	number_of_clusters = 100
	topological_sorting_file = None
	root_node = "Category:Main_topic_classifications"
	graph_depth = 3
	n_nodes = 1000

	if from_dbpedia:
		G = make_wiki_adjacencies.add_adjacencies(graph_manip.DiGraph(),input_file)
	else:
		G = graph_manip.load_graph(input_file)
	#could also use popularity to weight random sampling
	new_graph = graph_manip.sample_graph(G, n_nodes)

	graph_manip.compute_clustering(G, [new_graph], number_of_clusters, cluster_groupings_file, cluster_names_file, topological_sorting_file)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()

	parser.add_argument("input_file")
	parser.add_argument("cluster_groupings_file")
	parser.add_argument("cluster_names_file")
	parser.add_argument("-d", "--from_dbpedia", action="store_true")

	args = parser.parse_args()

	main(args.input_file,args.cluster_groupings_file,args.cluster_names_file,from_dbpedia=args.from_dbpedia)
