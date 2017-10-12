
import pd

def get_data(dataset_file):
	with open(dataset_file, "r") as dataset:
		print("reading csv file ("+dataset_file+")")
		df = pd.read_csv(dataset)
		names = []
		X = []
		if df.shape[1] == 3:
			y = []
		elif df.shape[1] == 2:
			y = None
		else:
			raise Exception("wrong dataset file format")

		for i,row in df.iterrows():
			article = eval(row[1])
			if type(article[1]) != type(None):
				names.append(article[0])
				X.append(article[1])
				if df.shape[1] == 3:
					y.append(eval(row[2]))
			if (i+1)%10000 == 0 or i+1 == df.shape[0]:
				print(str(i+1)+" / "+str(df.shape[0]))
				
	return names, X, y