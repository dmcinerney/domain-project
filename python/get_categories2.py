import graph_manip
import make_wiki_adjacencies

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()

	parser.add_argument("input_file")
	parser.add_argument("cluster_groupings_file")
	parser.add_argument("cluster_names_file")
	parser.add_argument("-d", "--from_dbpedia", action="store_true")

	args = parser.parse_args()

	input_file = args.input_file
	from_dbpedia = args.from_dbpedia
	output_file = "categories.txt"
	number_of_clusters = 100
	cluster_mappings_file = "cluster_mappings.txt"
	cluster_groupings_file = args.cluster_groupings_file
	cluster_names_file = args.cluster_names_file
	topological_sorting_file = "topological_sorting.txt"
	root_node = "Category:Main_topic_classifications"
	graph_depth = 3

	if from_dbpedia:
		G = make_wiki_adjacencies.add_adjacencies(graph_manip.DiGraph(),input_file)
	else:
		G = graph_manip.load_graph(input_file)
	new_graph = graph_manip.get_n_level_graph_from(G, root_node, graph_depth)

	graph_manip.compute_clustering(G, [new_graph], number_of_clusters, cluster_mappings_file, cluster_groupings_file, cluster_names_file, topological_sorting_file)
	
	with open(output_file, "w") as outfile:
		for node in new_graph.nodes():
			outfile.write(node+"\n")

