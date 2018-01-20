#!/usr/bin/env python


def predict(RD, RIA, RIS, RRV, RWR, num_courses):
  from sklearn.model_selection import GridSearchCV
  from sklearn.model_selection import StratifiedShuffleSplit
  from sklearn.model_selection import train_test_split
  from sklearn.svm import SVC
  import pandas as pd
  import numpy as np

  model_df = pd.read_csv('../src/Data/allcourses.csv')
  model_df = model_df.iloc[:, 1:]
  model_df.drop(labels=['Rec Major', 'Rec Non Major'], axis=1, inplace=True)

  # Calculate ranks along columns
  ranks_df = model_df.iloc[:, 2:].rank(axis=1)
  rank_columns = ['RD', 'RIA', 'RIS', 'RRV', 'RWR']
  ranks_df.columns = rank_columns
  ranks_df = pd.concat([ranks_df, model_df], axis=1)

  ranks_df['Label'] = ranks_df[ranks_df.columns[:5]].apply(lambda x: ''.join(x.dropna().astype(int).astype(str)), axis=1)
  ranks_df['Label'] = ranks_df['Label'].astype(int)

  # Get rid of columns with ranks as this is now captures in Label
  ranks_df.drop(labels=rank_columns, axis=1, inplace=True)

  # Obtain the number of unique courses under each label
  counts = ranks_df['Label'].value_counts()

  # Only keep those labels with more than one sample per label
  labels_tokeep = counts[counts > 1]

  # Remove samples with undesired labels from dataframe
  final_df = ranks_df[ranks_df['Label'].isin(labels_tokeep.index)]

  # split data into features and labels for model
  x = final_df.iloc[:, 2:-1]
  y = final_df['Label']

  svm_clf = SVC()
  svm_clf.fit(x, y)

  ################################################
  # Making prediction
  ################################################
  random_vec = np.asarray([RD, RIA, RIS, RRV, RWR])
  random_vec = random_vec.reshape(1, -11)
  class_pred = svm_clf.predict(random_vec)[0]

  pred_df = final_df.loc[final_df['Label'] == class_pred]
  return pred_df['Course Alias'].tolist()[:num_courses]

