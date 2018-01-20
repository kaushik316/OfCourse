#!/usr/bin/env python

from auth import api_key
import requests, json, os

class Dept:

  def __init__(self, path, ID, name):
    self.path = path
    self.ID = ID
    self.name = name


class Course:

  def __init__(self, path, ID, name, aliases):
    self.path = path
    self.ID = ID
    self.name = name.replace(',', '')
    self.aliases = aliases
    self.get_primary_alias()
    self.get_description()

  def get_primary_alias(self):
    r = search(self.path)
    data = json.loads(r.text)
    self.primary_alias = data['result']['courses'][0]['primary_alias']

  def get_description(self):
    r = search('courses/%s' % self.ID)
    data = json.loads(r.text)
    self.description = data['result']['description'].replace(',', '|').replace('\n', ' ')

def search(path):
  """
  Gets data from the PennLabs API at "path"
  """
  base_url = 'http://api.penncoursereview.com/v1/'
  url = base_url + path + '?token={}'
  url = url.format(api_key)
  return requests.get(url)

def get_departments():
  """
  Returns a list of Dept objects describing Departments at Penn
  """
  r = search('depts')
  data = json.loads(r.text)
  departments = data['result']['values']
  return [Dept(d['path'],d['id'],d['name']) for d in departments]

def get_dept_courses(dept):
  """
  Gets full list of courses for a given dept from PennLabs API
  returns a list of Course objects describing courses in given department:
  """
  r = search(dept.path)
  data = json.loads(r.text)
  course_histories = data['result']['coursehistories']
  return [Course(c['path'], c['id'], c['name'], c['aliases']) for c in course_histories]

def generate_dept_csv(dept):
  print("[*] Accessing %s Department" % dept.ID)
  with open('Departments/%s_courses.csv' % dept.ID, 'w') as f:
    f.write('NAME,ALIAS,PATH,DESCRIPTION\n')
    courses = get_dept_courses(dept)
    num_courses = len(courses)
    for i, course in enumerate(courses):
      f.write("%s,%s,%s,%s\n" % (course.name, course.primary_alias, course.path, course.description))

def generate_csvs():
  if not os.path.isdir('Departments'):
    os.mkdir('Departments')
  depts = get_departments()
  for dept in depts:
    if os.path.isfile('Departments/%s_courses.csv' % dept.ID):
      continue 
    generate_dept_csv(dept)

 
if __name__=='__main__':
  generate_csvs()
