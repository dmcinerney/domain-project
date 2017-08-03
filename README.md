# domain-project
## Data

The dataset for this project will be coming primarily from the dbpedia website at the following address:

1. English skos categories file (with the ttl extension) - used to construct a graph of the connections between Wikipedia category pages
2. Article categories file (with the ttl extension) - used to link the articles to their categories
3. Wikipedia XML source dump file (with the xml extension) - used to get the articles in Wikipedia
<> (4. english redirects file (with the ttl extension) - used to get all titles of each article (This is not currently used in the repo but may be used in the future.))
<> (The version of Wikipedia stored at JHU CLSP in the concrete format (see http://hltcoe.github.io) may also be used later on.)

In addition to the Wikipedia dataset, this project also uses the GloVe (Global Vectors for Word Representation) files from the following website: https://nlp.stanford.edu/projects/glove/.

## Repository Structure

The repository is structured into two main code folders, "python" and "scripts".

"python" contains all of the helper scripts that run all of the specific tasks in the pipeline.  It is separated into a "Preprocessing" folder and a "QueryTimeProcessing" folder.

Preprocessing:
1. make_wiki_adjacencies.py - constructs graph for all categories in wikipedia and writes it to a file
		* Input: the skos categories file
		* Output: adjacencies.txt (enumerates nodes followed by adjacency list)
2. graph_manip.py
3. get_categories*.py - There are a few different versions of this script.  Each version has the same inputs and outputs.
		* Input: adjacencies.txt - the adjacencies file made from make_wiki_adjacencies script
		* Outputs: cluster_groupings.pkl (enumerates categories for each cluster), cluster_names.pkl (enumerates a name for each cluster)
4. get_article_dataset.py
		* Inputs: indices.pkl, vectors.npy
		* Output: dataset.csv, dataset_train.csv, dataset_dev.csv
5. stats.py - computes the statistics for the dataset
		* Input: dataset.csv
		* Outputs: stats.csv
6. train_classifiers.py - trains the classifiers for each cluster
		* Input: dataset file
		* Output: classifiers file
7. scrapped_scripts - a bunch of scripts that were used and are no longer used may be usefull to keep around.

QueryTimeProcessing:
1. DomainClassifier.py - a class for a classifier object that can classify an article into a domain term.

"scripts" contains two scripts, "preprocessing", which simply runs the whole preprocessing pipeline by calling scripts in the python/Preprocessing folder, and "querytime_processing", which runs the query-time processing pipeline by calling scripts in the python/QueryTimeProcessing folder (just the DomainClassifier.py file for now because most of the work is done in the querytime_processing.py script).

## Caches and Model storage

The scripts being run in both the preprocessing and query-time processing pipelines output files, some of which need to be used by other scripts in the pipeline.  Therefore cache's have been set up for each of the two pipelines called "temp_preprocessing*" and "temp_querytime*" (where the stars are replaced with numbers).  These caches are created automatically but can be reused and edited depending on options (see options section).

In addition the preprocessing pipeline needs to output models to be used in the query-time processing pipeline.  The models are placed in a folder called models.

## Pipeline Script Arguments and Options

Preprocessing:
	Not optional arguments:
		"path_to_repository"

	Optional string arguments:
		"-l", "--category_links_file", type=str, default=None
		"-e", "--embeddings_file", type=str, default=None
		"-c", "--article_categories_file", type=str, default=None
		"-r", "--article_redirects_file", type=str, default=None
		"-w", "--wiki_concrete_directory", type=str, default=None
		"-S", "--save_cache_as", type=str, default=None
		"-C", "--classifier_type", type=str, default="knn_multi"

	True/False options:
		"-m", "--make_adjacencies", action="store_true"
		"-g", "--get_categories", action="store_true"
		"-v", "--create_vectors_file", action="store_true"
		"-d", "--make_dataset", action="store_true"
		"-s", "--compute_stats", action="store_true"
		"-t", "--train_classifiers", action="store_true"

Query-time Processing:
	Not optional arguments:
		"path_to_repository"

	Optional string arguments:
		"-q", "--query_term", type=str, default=None
		"-a", "--articles_file", type=str, default=None
		"-e", "--embeddings_file", type=str, default=None
		"-O", "--classifier_option", type=str, default=None
		"-S", "--save_cache_as", type=str, default=None

	True/False options:
		"-d", "--use_dev_set", action="store_true"
