#!/usr/bin/env python
import flask 
import pymongo
from pymongo import MongoClient

app = flask.Flask(__name__)

@app.route('/')
def hello_world():
    con = MongoClient('localhost',5000)
    if con:
        return 'Database is working!\n'
    else: 
        return 'Database is not working\n'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 4000, debug=True)     # open for everyone
