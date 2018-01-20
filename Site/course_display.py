#!/usr/bin/env python

class Course_Display:

  def __init__(self, alias):
    self.alias = alias
    self.dept = alias.split('-')[0]
    self.get_name_descr()
    self.get_course_info()

  def get_name_descr(self):
    with open("../src/Departments/%s_courses.csv" % self.dept, 'r') as f:
      for course in f:
        c = course.strip().split(",")
        if (self.alias == c[1]):
          self.name = c[0]
          self.description = c[3]
          return

  def get_course_info(self):
    with open("../src/MostRecentSections/%s_courses.csv" % self.dept, 'r') as f:
      for course in f:
        c = course.strip().split(",")
        if (self.alias == c[0]):
          self.instructor = c[2]
          self.semester = c[1]
          self.quality = c[3]
          self.difficulty = c[4]
          self.instr_quality = c[5]
          self.stim_interest = c[6]
          self.work_req = c[7]

if __name__=='__main__':
  cd = Course_Display("CIS-110")

