#!/usr/bin/env python
import flask
from pymongo import MongoClient

app = flask.Flask(__name__)

@app.route('/')
def hello_world():
    client = MongoClient('localhost',4000)
    try:
        client.admin.command('ismaster')
        return 'Database working\n'
    except Exception:
        return 'Database is not working\n'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)     # open for everyone
