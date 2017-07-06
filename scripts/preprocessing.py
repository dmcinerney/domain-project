#This is the script to run the complete pre-processing pipeline
#this script should be run from the bottom level of the package

#example command line run:
#python domain-project/scripts/preprocessing.py domain-project/ -l skos_categories_en.ttl -c article_categories_en.ttl -w /export/corpora4/concrete/wiki-en/ -m -g -d -t

if __name__ == '__main__':
	import argparse
	import os
	import sys
	parser = argparse.ArgumentParser()

	#FIXME: may want to add "help=" to all of these
	parser.add_argument("path_to_repository")
	parser.add_argument("-l", "--category_links_file", type=str, default=None)
	parser.add_argument("-c", "--article_categories_file", type=str, default=None)
	parser.add_argument("-r", "--article_redirects_file", type=str, default=None)#may not include NOT CURRENTLY USED
	parser.add_argument("-w", "--wiki_concrete_directory", type=str, default=None)
	parser.add_argument("-m", "--make_adjacencies", action="store_true")
	parser.add_argument("-g", "--get_categories", action="store_true")
	parser.add_argument("-v", "--create_vectors_file", action="store_true")
	parser.add_argument("-d", "--make_dataset", action="store_true")
	parser.add_argument("-t", "--train_classifiers", action="store_true")
	parser.add_argument("-s", "--start_from_scratch", action="store_true")

	args = parser.parse_args()

	initial_working_directory = os.getcwd()

	#preprocessing path names
	path_to_repository = os.path.join(initial_working_directory,args.path_to_repository)
	sys.path.append(path_to_repository)#FIXME: there is a lot of commentary on this, not sure if it's the right way to do it
	models_folder = os.path.join(path_to_repository,"models")
	preprocessing_folder = os.path.join(path_to_repository,"python/Preprocessing")

	#handling cache folder
	temp_folder = os.path.join(path_to_repository,"temp_preprocessing0")
	if args.start_from_scratch:
		i = 0
		while os.path.isdir(temp_folder):
			i += 1
			temp_folder = temp_folder[:-len(str(i-1))] + str(i)
		if i >= 5:
			raise Exception("You should clean up your caches! There are already "+str(i)+" of them. No more are allowed. :(")
	if not os.path.isdir(temp_folder):
		os.system("mkdir "+temp_folder)
	else:
		print("defaulting to using \"temp_processing0\" as the curret cache")

	#preprocessing file names
	adjacencies_file = os.path.join(temp_folder,"adjacencies.txt")
	cluster_groupings_file = os.path.join(temp_folder,"cluster_groupings.txt")
	cluster_names_file = os.path.join(temp_folder,"cluster_names.txt")
	dataset_file = os.path.join(temp_folder,"dataset.csv")
	indices_file = os.path.join(temp_folder,"indices.pkl")
	vectors_file = os.path.join(temp_folder,"vectors.npy")
	classifiers_file = os.path.join(models_folder,"classifiers.pkl")

	#run preprocessing pipeline
	if args.make_adjacencies:
		if not args.category_links_file:
			raise Exception("no category links file!")
		print("MAKING ADJACENCIES")
		'''
		command = "python "+os.path.join(preprocessing_folder,"make_wiki_adjacencies.py")+" "+args.category_links_file+" "+adjacencies_file
		print(command)
		os.system(command)
		'''
		import python.Preprocessing.make_wiki_adjacencies as make_adjacencies
		make_adjacencies.main(args.category_links_file,adjacencies_file)
	if args.get_categories:
		print("GETTING CATEGORIES")
		'''
		command = "python "+os.path.join(preprocessing_folder,"get_categories2.py")+" "+adjacencies_file+" "+cluster_groupings_file+" "+cluster_names_file
		print(command)
		os.system(command)
		'''
		import python.Preprocessing.get_categories2 as getcategories
		getcategories.main(adjacencies_file,cluster_groupings_file,cluster_names_file)
	if args.create_vectors_file:
		print("CREATING VECTOR FILES")
		if not args.wiki_concrete_directory:
			raise Exception("no concrete wikipedia directory!")
		#FIXME: Need to do whatever Zhenya does to create the vectors file
		#step 1: run script to create vector file named vectors_file
		#step 2: create a pickled vectorizor object file to convert articles during prediction time
		raise NotImplementedError
	if args.make_dataset:
		if not args.article_categories_file:
			raise Exception("no article categories file!")
		print("GETTING ARTICLE DATASET")
		'''
		command = "python "+os.path.join(preprocessing_folder,"get_article_dataset.py")+" "+args.article_categories_file+" "+adjacencies_file+" "+cluster_groupings_file+" "+cluster_names_file+" "+vectors_file+" "+dataset_file
		print(command)
		os.system(command)
		'''
		import python.Preprocessing.get_article_dataset as makedataset
		makedataset.main(args.article_categories_file,adjacencies_file,cluster_groupings_file,cluster_names_file,indices_file,vectors_file,dataset_file)
	if args.train_classifiers:
		print("TRAINING CLASSIFIERS")
		'''
		command = "python "+os.path.join(preprocessing_folder,"train_classifiers.py")+" "+dataset_file+" "+classifiers_file
		print(command)
		os.system(command)
		'''
		import python.Preprocessing.train_classifiers as trainclassifiers
		trainclassifiers.main(dataset_file,classifiers_file)
