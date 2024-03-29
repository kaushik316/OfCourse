import pickle
import pandas as pd
import numpy as np


def return_random_sample(df):
	course = df.sample(n=1)
	course_alias = course['Course Alias'].iloc[0]
	course_rv = course['Readings Value'].iloc[0]
	return (course_alias, course_rv)

def filter_major(df):
	pass

def return_course(input_array):
	with open('Pickled/svm.pickle', 'rb') as model_file:
		svm_clf = pickle.load(model_file)

	with open('Pickled/final_df.pickle', 'rb') as df_file:
		final_df = pickle.load(df_file)

	# Predict label
	class_pred = svm_clf.predict(input_array)[0]
	print class_pred

	# Obtain value of reading for predicted course

	# Create a subset of courses that match the preferences
	pred_df = final_df.loc[final_df['Label'] == class_pred]

	# Return a random course from the matched subset
	alias, reading_value = return_random_sample(pred_df)
	print "The recommended course RV {}".format(reading_value)
	return (alias, reading_value)


if __name__ == "__main__":
	random_vec = np.asarray([2.2, 3.8, 3.5, 3.4, 2.3])
	random_vec = random_vec.reshape(1, -1)
	rec_course_alias, rec_course_rv = return_course(random_vec)
	print "Course ID: {}".format(rec_course_alias)