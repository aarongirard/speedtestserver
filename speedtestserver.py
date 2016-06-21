import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
	render_template, flash

#create the application
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'BOOBS'

#To set to a specific ip app.run(host="192.168.1.7",port=5010) handy if your pc has a few ip's
app.run(host="192.168.0.39", port = 5000)
