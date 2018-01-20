from auth import api_key
import requests
import pprint 
import pandas as pd
import json

course_df = pd.read_csv('Departments/AAMW_courses.csv')
print course_df.head()
course_ids = course_df['ALIAS']

for index, alias in enumerate(course_ids):
	url = "http://api.penncoursereview.com/v1/coursehistories/{}/reviews?token={}".format(alias, api_key)
	r = requests.get(url)

	# load api response into a dictionary
	data = json.loads(r.text)
	reviews = data["result"]["values"]

	# store course information to be used as features
	review_dict = {}
	features = ['rDifficulty', 'rStimulateInterest', 'rRecommendMajor','rWorkRequired',
			    'rInstructorAccess', 'rReadingsValue', 'rRecommendNonMajor']

	for feature in features:
		review_dict[feature] = []

	# iterate through all reviews for a given course and store features
	for review in reviews:
		for feature in features:
			# check if feature exists in this particular review
			if feature in review['ratings']:
				# if it does, get the numeric rating value for that category and add to dictionary
				rating = float(review['ratings'][feature])
				review_dict[feature].append(rating)

	# Only store the average value for each feature
	for k in review_dict.keys():
		rating_list = review_dict[k]

		# Make sure data exists for this feature 
		if len(rating_list) > 0:
			avg_rating = sum(rating_list)/len(rating_list)
			review_dict[k] = round(avg_rating, 2)

		else:
			review_dict[k] = None

	# Attach course name and id to set of reviews in dictionary
	review_dict['Alias'] = alias
	review_dict['Name'] = course_df['NAME'][index] 

	# Create a dataframe to hold all the course review values
	if index == 0:
		output_df = pd.DataFrame({'Difficulty': review_dict['rDifficulty'],
						  	   	  'Interest Score': review_dict['rStimulateInterest'],
			                      'Rec Major': review_dict['rRecommendMajor'],
			                      'Rec Non Major': review_dict['rRecommendNonMajor'],  
			                      'Work Required': review_dict['rWorkRequired'], 
			                      'Instructor Access': review_dict['rInstructorAccess'], 
			                      'Readings Value': review_dict['rReadingsValue'],	
			                      'Course Alias': review_dict['Alias'],
			                      'Course Name': review_dict['Name']
			                      }, index=[index])

	else:
		df_to_append = pd.DataFrame({ 'Difficulty': review_dict['rDifficulty'],
							  	   	  'Interest Score': review_dict['rStimulateInterest'],
				                      'Rec Major': review_dict['rRecommendMajor'],
				                      'Rec Non Major': review_dict['rRecommendNonMajor'],  
				                      'Work Required': review_dict['rWorkRequired'], 
				                      'Instructor Access': review_dict['rInstructorAccess'], 
				                      'Readings Value': review_dict['rReadingsValue'],	
				                      'Course Alias': review_dict['Alias'],
			                      	  'Course Name': review_dict['Name']
			                        }, index=[index])

		output_df = output_df.append(df_to_append)


# Get rid of data with missing values
output_df.dropna(how='any', inplace=True)
output_df.to_csv('Data/allcourses.csv')
