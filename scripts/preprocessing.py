#This is the script to run the complete pre-processing pipeline
#this script should be run from the bottom level of the package

#example command line run:
#python domain-project/scripts/preprocessing.py domain-project/ -l skos_categories_en.ttl -c article_categories_en.ttl -w /export/corpora4/concrete/wiki-en/ -m -g -d -t

if __name__ == '__main__':
	import argparse
	import os
	parser = argparse.ArgumentParser()

	parser.add_argument("path_to_repository")
	parser.add_argument("-l", "--category_links_file", type=str, default=None)
	parser.add_argument("-c", "--article_categories_file", type=str, default=None)
	parser.add_argument("-r", "--article_redirects_file", type=str, default=None)#may not include
	parser.add_argument("-w", "--wiki_concrete_directory", type=str, default=None)
	parser.add_argument("-m", "--make_adjacencies", action="store_true")
	parser.add_argument("-g", "--get_categories", action="store_true")
	parser.add_argument("-d", "--make_dataset", action="store_true")
	parser.add_argument("-t", "--train_classifiers", action="store_true")
	parser.add_argument("-s", "--start_from_scratch", action="store_true")

	#temp file names
	adjacencies_file = "temp/adjacencies.txt"
	cluster_groupings_file = "temp/cluster_groupings.txt"
	cluster_names_file = "temp/cluster_names.txt"
	dataset_file = "temp/dataset.csv"

	args = parser.parse_args()
	if args.start_from_scratch:
		os.system("rm -r temp")
	if not os.path.isdir("temp"):
		os.system("mkdir temp")

	if args.path_to_repository:
		path_to_repository = args.path_to_repository
	else:
		path_to_repository = ""
	path_to_repository = path_to_repository+"python/"

	#run pipeline
	if args.make_adjacencies:
		if not args.category_links_file:
			raise Exception("no category links file!")
		print("MAKING ADJACENCIES")
		os.system("python "+path_to_repository+"make_wiki_adjacencies.py "+args.category_links_file+" "+adjacency_file)
	if args.get_categories:
		print("GETTING CATEGORIES")
		os.system("python "+path_to_repository+"get_categories2.py "+adjacencies_file+" "+cluster_groupings_file+" "+cluster_names_file)
	if args.make_dataset:
		if not args.wiki_concrete_directory:
			raise Exception("no concrete wikipedia directory!")
		if not args.article_categories_file:
			raise Exception("no article categories file!")
		print("GETTING ARTICLE DATASET")
		os.system("python "+path_to_repository+"get_article_dataset.py "+args.wiki_concrete_directory+" "+args.article_categories_file+" "+adjacencies_file+" "+cluster_groupings_file+" "+cluster_names_file+" "+dataset_file)
	if args.train_classifiers:
		print("TRAINING CLASSIFIERS")
		pass
