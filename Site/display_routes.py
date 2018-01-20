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
    input_course_diff = 3
  if not input_inst_acc:
    input_inst_acc = 3
  if not input_stud_int:
    input_stud_int = 3
  if not input_value_read:
    input_value_read = 3
  if not input_work_req:
    input_work_req = 3
  return render_template('landing.html', 
    input_major = str(input_major),
    input_kw = str(input_kw),
    input_course_diff = str(input_course_diff),
    input_inst_acc = str(input_inst_acc),
    input_stud_int = str(input_stud_int),
    input_value_read = str(input_value_read),
    input_work_req = str(input_work_req))


# Accesses the display info for the result of the course predictor
@app.route('/display', methods = ['GET', 'POST'])
def display():

  # Get input from user, feed into 'predict()'
  from predict import *
  RD = 2.5
  RIA = 2.5
  RIS = 2.5
  RRV = 2.5
  RWR = 2.5
  num_courses = 2
  aliases = predict(RD, RIA, RIS, RRV, RWR, num_courses)
  print aliases


  alias = "CIS-110"
  from course_display import Course_Display
  return render_template('display.html', course = Course_Display(alias))

if __name__=='__main__':
  app.run(debug=True)
