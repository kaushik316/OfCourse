#!/usr/bin/env python

from flask import Flask, render_template, request

from os import listdir
import datetime

app = Flask(__name__)

#  The main view of CryptoGuru Invemestment Analyzer
@app.route('/', methods = ['GET', 'POST'])
def landing():
  input_major = request.form.get('major')
  input_kw = request.form.get('kw')
  input_course_diff = request.form.get('course_diff')
  input_inst_acc = request.form.get('inst_acc')
  input_stud_int = request.form.get('stud_int')
  input_value_read = request.form.get('value_read')
  input_work_req = request.form.get('work_req')
  if not input_kw:
    input_kw = 'test_input'
  if not input_course_diff:
    input_course_diff = 3.0
  if not input_inst_acc:
    input_inst_acc = 3.0
  if not input_stud_int:
    input_stud_int = 3.0
  if not input_value_read:
    input_value_read = 3.0
  if not input_work_req:
    input_work_req = 3.0

  course1 = display(input_course_diff, input_inst_acc, input_stud_int, input_value_read, input_work_req)
  if (len(course1.description) > 400):
    course1_concat = course1.description[:400] + "..."
  else:
    course1_concat = course1.description

  return render_template('landing.html', 
    input_major = str(input_major),
    input_kw = str(input_kw),
    input_course_diff = str(course1.difficulty),
    input_inst_acc = str(course1.instr_quality),
    input_stud_int = str(course1.stim_interest),
    input_value_read = str(input_value_read),
    input_work_req = str(course1.work_req),
    course1_name = course1.name,
    course1_acc= '85%',
    course1_summ = course1_concat,
    course1_inst_name = str(course1.instructor),
    course1_semester = str(course1.semester),
    course1_alias = str(course1.alias))


# @app.route('/display', methods = ['GET', 'POST'])
def display(RD_I, RIA_I, RIS_I, RRV_I, RWR_I):

  # Get input from user, feed into 'predict()'
  from recommend_course import *
  RD = RD_I
  RIA = RIA_I
  RIS = RIS_I
  RRV = RRV_I
  RWR = RWR_I
  # num_courses = 2
  # aliases = predict(RD, RIA, RIS, RRV, RWR, num_courses)
  # print aliases
  input_vector = np.asarray([RD, RIA, RIS, RRV, RWR])
  input_vector = input_vector.reshape(1, -1)
  alias = return_course(input_vector)
  from course_display import Course_Display
  course = Course_Display(alias)
  return course
  # return render_template('display.html', course = Course_Display(alias))

if __name__=='__main__':
  app.run(debug=True)
