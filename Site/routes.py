#!/usr/bin/env python

from flask import Flask, render_template, request

from os import listdir
import datetime

app = Flask(__name__)

#  The main view of CryptoGuru Invemestment Analyzer
@app.route('/', methods = ['GET', 'POST'])
def landing():
    return render_template('landing.html')

if __name__=='__main__':
  app.run(debug=True)
