from auth import api_key
import requests
import pprint 
import json

url = "http://api.penncoursereview.com/v1/coursehistories/JWST-162/reviews?token={}".format(api_key)
r = requests.get(url)

# load api response into a dictionary
data = json.loads(r.text)
reviews = data["result"]["values"]
print reviews[0]

# store course information to be used as features
review_dict = {}
features = ['Difficulty', 'StimulateInterest', 'RecommendMajor','rWorkRequired', 'InstructorAccess', 'ReadingsValue', 'RecommendNonMajor']

for feature in features:
	review_dict[feature] = []

# iterate through all reviews for a given course and store features
for review in reviews:
	for feature in features:
		rating = review_dict['ratings'][feature]
		review_dict[feature].append(rating)


print review_dict