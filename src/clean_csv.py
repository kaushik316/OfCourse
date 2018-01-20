import pandas as pd

'''
Helper functions
'''
def drop_empties(csv_path):
	df = pd.read_csv(csv_path)
	df = df.dropna(how='any')
	df.to_csv(csv_path)

def add_headers(csv_path):
	cols = ['Course Alias', 'Course Name', 'Difficulty','Instructor Access',
			 'Interest Score', 'Readings Value', 'Work Required']
	df = pd.read_csv(csv_path)
	df = df.drop(df.iloc[:, :2], axis=1)
	df.columns = cols
	df.to_csv('Data/allcourses_proc.csv')

add_headers('Data/allcourses_final.csv')
