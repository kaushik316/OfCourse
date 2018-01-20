from auth import api_key
import requests
import pprint 
import json

url = "http://api.penncoursereview.com/v1/coursehistories/JWST-162/reviews?token={}".format(api_key)
r = requests.get(url)
print r.text

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
	avg_rating = sum(rating_list)/len(rating_list)
	review_dict[k] = round(avg_rating, 2)

pprint.pprint(review_dict)