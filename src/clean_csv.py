import pandas as pd

'''
Allcourses should contain all feature columns with some missing
values. Drop any rows with missing values and save csv file
'''
def drop_empties(csv_path):
	df = pd.read_csv(csv_path)
	df = df.dropna(how='any')
	df.to_csv(csv_path)