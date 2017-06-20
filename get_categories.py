import graph_manip

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()

	parser.add_argument("adjacencies_file")

	args = parser.parse_args()

	number_of_clusters = 100
	cluster_mappings_file = "cluster_mappings.txt"
	cluster_groupings_file = "cluster_groupings.txt"
	cluster_names_file = "cluster_names.txt"
	topological_sorting_file = "topological_sorting.txt"

	G = graph_manip.load_graph(args.adjacencies_file,verbose=True)
	new_graph = graph_manip.trim_graph_nodes(G, iterations=100, useless_cuttoff=0, root="Category:Main_topic_classifications")
	components = sorted(graph_manip.weakly_connected_components(new_graph), key=len)
	components = [graph_manip.subgraph(new_graph, list(vertices)) for vertices in components]
	print("total number of components before trimming: "+str(len(components)))
	components = graph_manip.trim_subgraphs(components, subgraph_cuttoff=100, n_top_nodes=None)
	print("total number of components after trimming: "+str(len(components)))
	print()
	graph_manip.compute_clustering(G, components, number_of_clusters, cluster_mappings_file, cluster_groupings_file, cluster_names_file, topological_sorting_file)