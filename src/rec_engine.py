from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import pandas as pd
import numpy as np 

model_df = pd.read_csv('Data/allcourses.csv')
model_df = model_df.iloc[:, 1:]
model_df.drop(labels=['Rec Major', 'Rec Non Major'], axis=1, inplace=True)

# Calculate ranks along columns
ranks_df = model_df.iloc[:, 2:].rank(axis=1)
rank_columns = ['RD', 'RIA', 'RIS', 'RRV', 'RWR']
ranks_df.columns = rank_columns
ranks_df = pd.concat([ranks_df, model_df], axis=1)

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
X = final_df.iloc[:, 2:-1]
y = final_df['Label']

print y.value_counts()

# Parameter grid for grid search
# Omit C values from the grid as class_weight param does this automatically for us
# svm_parameters = {'kernel': ['linear', 'rbf'],
# 				  'gamma': [1e-1, 1e2, 5]}

# cv = StratifiedShuffleSplit(n_splits=5, test_size=0.2)
svm_clf = SVC()


# Split courses into training and testing data
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
svm_clf.fit(x_train, y_train)
svm_score = svm_clf.score(x_test, y_test)

print "score is {}".format(svm_score)
# grid = GridSearchCV(svm_clf, param_grid=svm_parameters, cv=cv)
# grid.fit(x_train, y_train)
# print("The best parameters are {0} with a score of {1:.2f}%".format(grid.best_params_, grid.best_score_))

# grid_score = grid.score(x_test, y_test)
# print "Grid search's score on new test data was {0:.2f}%".format(grid_score)


random_vec = np.asarray([2.16, 3.68, 3.55, 3.5, 2.32])
random_vec = random_vec.reshape(1, -11)
class_pred = svm_clf.predict(random_vec)[0]

print "class_pred: {}".format(class_pred)


pred_df = final_df.loc[final_df['Label'] == class_pred]
print pred_df.head()


