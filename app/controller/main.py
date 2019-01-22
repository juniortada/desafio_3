# Author: Junior Tada
from app import app, log
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return 'hello world!'
