#!/usr/bin/python3
import os, redis
from flask import Flask, Response
app = Flask(__name__)
db=redis.from_url(os.environ['REDISCLOUD_URL'])

@app.route('/')
def hello():
    savedlog=db.get('savedlog') or 'Hashnest bot by astrolince'
    return Response(savedlog, mimetype='text/plain')

@app.route('/get/<key>')
def get(key):
    key=db.get(key) or '404'
    return key

if __name__ == '__main__':
    app.run()
