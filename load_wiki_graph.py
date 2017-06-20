import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inputfile",type=str,default=None)
parser.add_argument("-x", "--x_clusters",type=int,default=2)
parser.add_argument("-a", "--adjacencies_file",type=str,default="adjacencies.txt")
parser.add_argument("-m", "--cluster_mappings_file",type=str,default="cluster_mappings.txt")
parser.add_argument("-g", "--cluster_groupings_file",type=str,default="cluster_groupings.txt")
parser.add_argument("-e", "--use_embeddings", action="store_true")
parser.add_argument("-c", "--compute_clustering", action="store_true")
parser.add_argument("-t", "--topological_sorting_file",type=str,default="topological_sorting.txt")
parser.add_argument("-n", "--cluster_names_file",type=str,default="cluster_names.txt")

args = parser.parse_args()
input_filename = args.inputfile
number_of_clusters = args.x_clusters
adjacencies_file = args.adjacencies_file
cluster_mappings_file = args.cluster_mappings_file
cluster_groupings_file = args.cluster_groupings_file
use_embeddings = args.use_embeddings
compute_clustering = args.compute_clustering
topological_sorting_file = args.topological_sorting_file
cluster_names_file = args.cluster_names_file

from networkx import *
import sys
import numpy as np

def get_embeddings():
	glovefile = "/Users/jeredmcinerney/Desktop/Intelellectual/glove/glove.6B.300d.txt"
	embeddings = {}
	with open(glovefile, 'r') as embeddings_file:
		for line in embeddings_file:
			linesplit = line.split()
			word = linesplit[0]
			values = [float(numstr) for numstr in linesplit[1:]]
			embeddings[word] = values
	print("done getting embeddings!")

	return embeddings

#takes in words and embeddings and calculates the final vector embedding and returns it in a numpy array
def get_embedding_rep(words, embeddings):
	final_vector = np.zeros(len(embeddings[embeddings.keys()[0]]))
	#print(final_vector)
	num_embedded_words = 0
	for i,word in enumerate(words):
		if word.lower() in embeddings.keys():
			final_vector = np.add(final_vector, np.array(embeddings[word.lower()]))
			num_embedded_words += 1
		else:
			print(word)
		#print(str(i)+" / "+str(len(words)), word)
	if num_embedded_words != 0:
		final_vector /= num_embedded_words

	return final_vector

def remove_nodes_if(G, should_remove):
	usefull_nodes = []
	for node in nodes_iter(G):
		if not should_remove(node):
			usefull_nodes.append(node)
	return subgraph(G, usefull_nodes)

def trim_graph_nodes(G, iterations=0, useless_cuttoff=0, root=None):
	if root or iterations:
		print("trimming graph nodes")
		print("\tcopying graph")
		new_graph = G.copy()
		if root:
			print("\tgetting subgraph consisting of descendants of "+root)
			new_graph = subgraph(new_graph, descendants(new_graph, root))
			print("\tnow has "+str(len(new_graph))+" nodes")
		if iterations:
			print("\ttrimming leaves")
			for i in range(iterations):
				initial_length = len(new_graph)
				new_graph = remove_nodes_if(new_graph, lambda x: len(new_graph.neighbors(x)) <= useless_cuttoff)
				print("\t\tremoved "+str(initial_length-len(new_graph))+" nodes")
				print("\t\t"+str(i+1)+" / "+str(iterations))
				if (initial_length-len(new_graph)) == 0:
					print("\tstopping iterations early")
					break
		print("done trimming graph nodes")
		return new_graph
	else:
		return G

#don't keep subgraphs that are less than n
#only keep top p of nodes in each subgraph
def trim_subgraphs(components, subgraph_cuttoff=None, n_top_nodes=None):
	print("trimming subgraphs")

	#cut unnecessary subgraphs

	new_components = []
	if subgraph_cuttoff:
		print("\tcutting subgraphs with under "+str(subgraph_cuttoff)+" nodes")
		print("\t\tinitial number of components: "+str(len(components)))
		for component in components:
			if len(component) > subgraph_cuttoff:
				print("\t\tadding component which has "+str(len(component))+" nodes")
				new_components.append(component)
		print("\t\tfinal number of components: "+str(len(new_components)))
	else:
		new_components = components

	if n_top_nodes:
		#get rid of cycles in remaining components
		print("\tmaking components into acyclic graphs")
		for i,component in enumerate(new_components):
			print("\t\tfinding cycles in graph with "+str(len(component))+" nodes")
			cycles = simple_cycles(component)
			print("\t\t"+str(len(list(cycles)))+" cycles found")
			for cycle in cycles:
				#print(cycle)
				if len(cycle) > 1:
					u, v = cycle[0], cycle[1]
				else:
					u, v = cycle[0], cycle[0]
				try:
					component.remove_edge(u, v)
				except exception.NetworkXError as e:
					print(e)
					continue
			print("\t\t"+str(i+1)+" / "+str(len(new_components)))

		#topologically sort remaining components and
		#get rid of all nodes except for top p
		print("\ttopologically sorting and cutting bottom nodes on the graphs")
		for component in new_components:
			component.remove_nodes_from(topological_sort(component)[n_top_nodes:])

		#expand components into not connected subgraphs and return final components
		print("\texpanding graphs into their connected subgraphs")
		new_components2 = []
		for component in new_components:
			new_components2.extend(weakly_connected_components(component))
		new_components = [subgraph(G, list(vertices)) for vertices in new_components2]
	print("done trimming subgraph")
	return sorted(new_components, key=len)


'''
n=10 # 10 nodes
m=20 # 20 edges

G=gnm_random_graph(n,m)
'''
G = DiGraph()
if input_filename != None:
	if use_embeddings:
		print("getting embeddings")
		dumbwords = []
		with open('stopwords.txt', 'r') as stopwords:
			for line in stopwords:
				if line[0] != "#":
					dumbwords.append(line.strip())
		embeddings = get_embeddings()
	print("loading from input dbpedia file ("+input_filename+")")
	import re
	beginningstr = "<http://dbpedia.org/resource/"
	endingstr = ">"
	pattern = re.compile(beginningstr+".*?"+endingstr)
	#load graph from wikipedia


	with open(input_filename, "r") as infile:
		for i,line in enumerate(infile):
			#if i > 1000: break
			splitline = line.strip().split()
			#print(splitline[0],splitline[2])
			page1 = re.findall(pattern,splitline[0])
			page2 = re.findall(pattern,splitline[2])
			if len(page1) == 0 or len(page2) == 0:
				if (i+1) % 100000 == 0: print(i+1)
				continue
			page1 = page1[0].replace(beginningstr,"").replace(endingstr,"")
			page2 = page2[0].replace(beginningstr,"").replace(endingstr,"")
			#print(page1,page2)
			G.add_node(page1)
			G.add_node(page2)
			if not use_embeddings:
				G.add_edge(page2,page1,weight=1.0)
			else:
				words1 = [word for word in page1[9:].split("_") if word not in dumbwords]
				words2 = [word for word in page2[9:].split("_") if word not in dumbwords]
				print(len(words1),len(words2))
				rep1 = get_embedding_rep(words1,embeddings)
				rep2 = get_embedding_rep(words2,embeddings)
				cosine_sim = np.dot(rep1,rep2)/(np.linalg.norm(rep1)*np.linalg.norm(rep2))

				G.add_edge(page2,page1,weight=cosine_sim)
			#FIXME: replace weight with cosine similarity
			if (i+1) % 100000 == 0: print(i+1)
	print("done loading graph")

	# write the adjacency list to file
	print("writing to file")
	with open(adjacencies_file,"w") as adjfile:
		for node in G.nodes():
			adjfile.write(node+" "+str([(n, G.edge[node][n]["weight"]) for n in G.neighbors(node)])+"\n")
	print("done writing to file")
else:
	print("loading from adjacencies file ("+adjacencies_file+")")
	with open(adjacencies_file,"r") as adjfile:
		for i,line in enumerate(adjfile):
			if i < 3: continue
			node = line.strip().split()[0]
			nodes = eval(line.strip()[len(node)+1:])
			nodenames = [n[0] for n in nodes]
			nodenames.append(node)
			G.add_nodes_from(nodenames)
			G.add_edges_from([(node,n[0],{"weight":float(n[1])}) for n in nodes])
			#FIXME: replace weight with cosine similarity
			if (i+1) % 100000 == 0: print(i+1)
	print("done loading graph")

### PRINT INFORMATION ABOUT GRAPH ###
print("INFORMATION ABOUT FULL GRAPH")
print("directed acyclic: "+str(is_directed_acyclic_graph(G)))
print("weakly connected: "+str(is_weakly_connected(G)))
n_nodes = len(G.nodes())
n_edges = len(G.edges())
print("total number of nodes before any trimming: "+str(n_nodes))
print("total number of edges before any trimming: "+str(n_edges))

### TRIM GRAPH ###
new_graph = trim_graph_nodes(G, iterations=100, useless_cuttoff=1, root="Category:Main_topic_classifications")
n_nodes = len(new_graph.nodes())
n_edges = len(new_graph.edges())
print("total number of nodes after graph trimming: "+str(n_nodes))
print("total number of edges after graph trimming: "+str(n_edges))

print("getting components")
components = sorted(weakly_connected_components(new_graph), key=len)
components = [subgraph(new_graph, list(vertices)) for vertices in components]
print("total number of components before trimming: "+str(len(components)))

### TRIM SUBGRAPHS ###
components = trim_subgraphs(components, subgraph_cuttoff=100, n_top_nodes=None)

print("total number of components after trimming: "+str(len(components)))
n_nodes = sum(len(component.nodes()) for component in components)
n_edges = sum(len(component.edges()) for component in components)
print("total number of nodes after subgraph trimming: "+str(n_nodes))
print("total number of edges after subgraph trimming: "+str(n_edges))

### CLUSTER ###
if compute_clustering:
	print("computing clustering")
	from sklearn import cluster as cl
	clusters = []
	topsort = []
	for i,graph in enumerate(components):
		print("\nthis is a "+str(len(graph))+"-node graph")
		is_acyclic = is_directed_acyclic_graph(graph)
		print("directed acyclic: "+str(is_acyclic))
		if is_acyclic:
			topsort.append(topological_sort(graph))
			print("\tdone with topological sort")
			print("\ttop 3 categories: "+str(topsort[-1][:3]))
		#print(m.todense())
		n = int(round(number_of_clusters*(float(len(graph))/float(n_nodes))))
		if n < 1:
			print("\tthis is 1 cluster")
			clusters.append(list(zip(graph.nodes(), [0]*len(graph))))
		else:
			print("\tdoing spectral clustering to produce "+str(n)+" clusters")
			#if len(graph) > 100000: print("jk, not gonna do this now"); continue
			print("\t\tcreating adjacency matrix")
			m = adjacency_matrix(graph.to_undirected())
			print("\t\tdone creating adjacency matrix")
			print("\t\tstarting clustering")
			#sp = cl.SpectralClustering(n_clusters=n, n_jobs=-1, affinity="precomputed")
			sp = cl.SpectralClustering(n_clusters=n, affinity="precomputed")
			clusters.append(list(zip(graph.nodes(), sp.fit_predict(m))))
		print(str(i+1)+" / "+str(len(components)))

	print("done clustering")
	#print(clusters)
	graphclusternum = 0
	cluster_groupings = {}
	cluster_mappings = []
	for graphcluster in clusters:
		for node, cluster in graphcluster:
			if str(graphclusternum)+" "+str(cluster) not in cluster_groupings.keys():
				cluster_groupings[str(graphclusternum)+" "+str(cluster)] = []
			cluster_groupings[str(graphclusternum)+" "+str(cluster)].append(node)
			cluster_mappings.append((node,str(graphclusternum)+" "+str(cluster)))
		graphclusternum += 1
	cluster_names = {}
	for clusterkey,nodes in cluster_groupings.items():
		subG = subgraph(G, nodes).to_undirected()
		centralities = betweenness_centrality(subG)
		node_centrality = max(((node,centrality) for node,centrality in centralities.items()), key=lambda x:x[1])
		cluster_names[clusterkey] = node_centrality[0]
	#print(cluster_mappings)
	#print(cluster_groupings)

	### WRITE TO FILES ###
	with open(cluster_mappings_file, "w") as mapfile:
		for nodename, cluster in cluster_mappings:
			mapfile.write(nodename+" "+str(cluster)+"\n")

	with open(cluster_groupings_file, "w") as groupfile:
		for cluster, nodes in cluster_groupings.items():
			groupfile.write(str(cluster)+" "+str(nodes)+"\n")

	with open(cluster_names_file, "w") as namesfile:
		for cluster, name in cluster_names.items():
			namesfile.write(str(cluster)+" "+name+"\n")

	with open(topological_sorting_file, "w") as topfile:
		for nodelist in topsort:
			for node in nodelist:
				topfile.write(node+"\n")
			topfile.write("\n")

