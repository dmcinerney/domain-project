import graph_manip

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()

	parser.add_argument("adjacencies_file")

	args = parser.parse_args()

	output_file = "categories.txt"
	number_of_clusters = 100
	cluster_mappings_file = "cluster_mappings.txt"
	cluster_groupings_file = "cluster_groupings.txt"
	cluster_names_file = "cluster_names.txt"
	topological_sorting_file = "topological_sorting.txt"

	G = graph_manip.load_graph(args.adjacencies_file)
	new_graph = graph_manip.get_n_level_graph_from(G, "Category:Main_topic_classifications", 5)

	with open(output_file, "w") as outfile:
		for node in new_graph.nodes():
			outfile.write(node+"\n")

	graph_manip.compute_clustering(G, components, number_of_clusters, cluster_mappings_file, cluster_groupings_file, cluster_names_file, topological_sorting_file)
	