#This is the script to run the complete pre-processing pipeline
#this script should be run from the bottom level of the package
'''
example command line run with every possible option used (except redirects) (runs whole pipeline):
python domain-project/scripts/preprocessing.py domain-project/ -l skos_categories_en.ttl -c article_categories_en.ttl -w /export/corpora4/concrete/wiki-en/ -m -g -v -d -s -t -S -C knn_multi

more common, less complex example command line run (doesn't run whole pipeline so must have a cache):
python domain-project/scripts/preprocessing.py domain-project/ -t -C knn_multi
'''
def save_cache(save_cache_as, path_to_repository, temp_folder):
	if save_cache_as:
		saved_caches_folder = os.path.join(path_to_repository,"saved_caches")
		if not os.path.isdir(saved_caches_folder):
			print("saving cache as \""+saved_cache+"\"")
			os.system("mkdir "+saved_caches_folder)
		saved_cache = os.path.join(saved_caches_folder,save_cache_as)
		i = 0
		while os.path.isfile(saved_cache):
			if i == 0:
				saved_cache = saved_cache+"_"+str(i)
			else:
				saved_cache = saved_cache[:-len(str(i-1))]+"_"+str(i)
			i += 1
		print("saving cache as \""+saved_cache+"\"")
		os.system("cp -r "+temp_folder+"/* "+saved_cache)

#FIXME: add a file to tell what settings were used
if __name__ == '__main__':
	import argparse
	import os
	import sys
	parser = argparse.ArgumentParser()

	#FIXME: may want to add "help=" to all of these
	parser.add_argument("path_to_repository")
	parser.add_argument("-l", "--category_links_file", type=str, default=None)
	parser.add_argument("-e", "--embeddings_file", type=str, default=None)
	parser.add_argument("-c", "--article_categories_file", type=str, default=None)
	parser.add_argument("-r", "--article_redirects_file", type=str, default=None)#FIXME: may not include NOT CURRENTLY USED
	parser.add_argument("-w", "--wiki_concrete_directory", type=str, default=None)
	parser.add_argument("-m", "--make_adjacencies", action="store_true")
	parser.add_argument("-g", "--get_categories", action="store_true")
	parser.add_argument("-v", "--create_vectors_file", action="store_true")
	parser.add_argument("-d", "--make_dataset", action="store_true")
	parser.add_argument("-s", "--compute_stats", action="store_true")
	parser.add_argument("-t", "--train_classifiers", action="store_true")
	parser.add_argument("-S", "--save_cache_as", type=str, default=None)
	parser.add_argument("-C", "--classifier_type", type=str, default="knn_multi")

	args = parser.parse_args()

	initial_working_directory = os.getcwd()

	#preprocessing path names
	path_to_repository = os.path.join(initial_working_directory,args.path_to_repository)
	sys.path.append(path_to_repository)#FIXME: there is a lot of commentary on this, not sure if it's the right way to do it
	models_folder = os.path.join(path_to_repository,"models")
	preprocessing_folder = os.path.join(path_to_repository,"python/Preprocessing")

	#handling cache folder
	temp_folder = os.path.join(path_to_repository,"temp_preprocessing")
	if not os.path.isdir(temp_folder):
		print("creating cache \""+temp_folder+"\"")
		os.system("mkdir "+temp_folder)
	#creating model file
	if not os.path.isdir(models_folder):
		print("making model folder \""+models_folder+"\"")
		os.system("mkdir "+models_folder)

	#preprocessing file names
	adjacencies_file = os.path.join(temp_folder,"adjacencies.txt")
	cluster_groupings_file = os.path.join(temp_folder,"cluster_groupings.pkl")
	cluster_names_file = os.path.join(temp_folder,"cluster_names.pkl")
	dataset_file_base = os.path.join(temp_folder,"dataset.csv")
	dataset_file_train = dataset_file_base[:-4]+"_train.csv" #may want to not do manually in the future
	indices_file = os.path.join(temp_folder,"indices.pkl")
	vectors_file = os.path.join(temp_folder,"vectors.npy")
	classifiers_file = os.path.join(models_folder,"classifiers.pkl")
	stats_file = os.path.join(temp_folder,"stats.csv")
	vectorizer_file = os.path.join(models_folder,"vectorizer.pkl")

	#run preprocessing pipeline
	if args.make_adjacencies:
		if not args.category_links_file:
			raise Exception("no category links file!")
		print("MAKING ADJACENCIES")
		import python.Preprocessing.make_wiki_adjacencies as make_adjacencies
		make_adjacencies.main(args.category_links_file,adjacencies_file,embeddings_file=args.embeddings_file)
	if args.get_categories:
		print("GETTING CATEGORIES")
		import python.Preprocessing.get_categories2 as getcategories
		#import python.Preprocessing.get_categories3 as getcategories
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
		import python.Preprocessing.get_article_dataset as makedataset
		makedataset.main(args.article_categories_file,cluster_groupings_file,indices_file,vectors_file,dataset_file_base,.2)
	if args.compute_stats:
		print("COMPUTING STATISTICS")
		import python.Preprocessing.stats as stats
		stats.main(dataset_file_train,stats_file)
	if args.train_classifiers:
		print("TRAINING CLASSIFIERS")
		import python.Preprocessing.train_classifiers as trainclassifiers
		trainclassifiers.main(cluster_names_file,dataset_file_train,classifiers_file,args.classifier_type)

	save_cache(args.save_cache_as, path_to_repository, temp_folder)
