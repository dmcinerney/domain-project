#This is the script to run the complete pre-processing pipeline

#here are the input files
CAT_LINKS_FILE = $1
ART_CATS_FILE = $2
ART_REDIR_FILE = $3
WIKI_CONCRETE_DIR = $4

#temp file names
ADJ_FILE = "temp/adjacencies.txt"


rm -r temp
mkdir temp

python make_wiki_adjacencies.py $CAT_LINKS_FILE $ADJ_FILE

python get_categories2.py $ADJ_FILE

python get_article_dataset.py ART_CATS_FILE ADJ_FILE cluster_groupings.txt cluster_names.txt
#need to fix to make get_categories take output file names as inputs and so can put them as variables
#also should itself take output files as input

