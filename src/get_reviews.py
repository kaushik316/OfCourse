from auth import api_key
import requests
import pprint 
import json


url = "http://api.penncoursereview.com/v1/coursehistories/JWST-162/reviews?token={}".format(api_key)
r = requests.get(url)
print(r.text)