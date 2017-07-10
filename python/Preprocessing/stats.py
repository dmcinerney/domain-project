#script gets stats about wikipedia and the clusters

def main(dataset_file):
	pass

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("dataset_file")

	args = parser.parse_args()

	main(args.dataset_file)
