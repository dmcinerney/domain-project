import graph_manip

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()

	parser.add_argument("adjacencies_file")

	args = parser.parse_args()

	output_file = "categories.txt"

	G = graph_manip.load_graph(args.adjacencies_file)
	new_graph = graph_manip.get_n_level_graph_from(G, "Category:Main_topic_classifications", 3)
	print(len(new_graph))
	with open(output_file, "w") as outfile:
		for node in new_graph.nodes():
			outfile.write(node+"\n")