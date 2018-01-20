"""
Data processing and machine learning model. Trains SVM, 
makes predictions based on input vector and saves model
"""

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import pandas as pd
import numpy as np 
import pickle


def return_random_sample(df):
	course = df.sample(n=1)
	course_alias = course['Course Alias'].iloc[0]
	course_name = course['Course Name'].iloc[0]
	return (course_alias, course_name)

# To save model and dataframes
def pickle_stuff(obj, path):
	with open(path, 'wb') as p_file:
		pickle.dump(obj, p_file)


model_df = pd.read_csv('Data/allcourses_proc.csv')

# count of non numeric columns in dataset
non_numeric_columns = 2

# Calculate ranks along columns
ranks_df = model_df.iloc[:, (non_numeric_columns + 1):].rank(axis=1)

rank_columns = ['RD', 'RIA', 'RIS', 'RRV', 'RWR']
ranks_df.columns = rank_columns
ranks_df = pd.concat([ranks_df, model_df], axis=1)

# Convert ranks to a string stored in a single column
ranks_df['Label'] = ranks_df[ranks_df.columns[:5]].apply(lambda x: ''.join(x.dropna().astype(int).astype(str)),axis=1)
ranks_df['Label'] = ranks_df['Label'].astype(int)

# Get rid of columns with ranks as this is now captures in Label
ranks_df.drop(labels=rank_columns, axis=1, inplace=True)

# Obtain the number of unique courses under each label
counts = ranks_df['Label'].value_counts() 

# Only keep those label with more than one sample per label
labels_tokeep = counts[counts > 1]

# Remove samples with undesired labels from dataframe
final_df = ranks_df[ranks_df['Label'].isin(labels_tokeep.index)]

# Split data into features and labels for model
X = final_df.iloc[:, (non_numeric_columns+ 1):-1]
y = final_df['Label']

svm_clf = SVC(kernel='linear', C=10)

# Split courses into training and testing data
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
svm_clf.fit(x_train, y_train)
svm_score = svm_clf.score(x_test, y_test)

print "score is {}".format(svm_score)

# Test a prediction on a synthetic sample
random_vec = np.asarray([2.16, 3.68, 3.55, 3.5, 2.32])
random_vec = random_vec.reshape(1, -1)
class_pred = svm_clf.predict(random_vec)[0]

# Create a subset of courses that match the preferences
pred_df = final_df.loc[final_df['Label'] == class_pred]

alias, name = return_random_sample(pred_df)
print "The recommended course is {}".format(name)
print "Course ID: {}".format(alias)


# Save model and final dataframe
pickle_stuff(svm_clf, "Pickled/svm.pickle")
pickle_stuff(final_df, "Pickled/final_df.pickle")



