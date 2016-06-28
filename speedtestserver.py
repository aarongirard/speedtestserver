import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
	render_template, flash

#create the application
app = Flask(__name__)

DB = 'SpeedTest.db'

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DB)
	return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def hello_world():
    return 'YOU ARE IN AARONS DOMAIN MOOOAHAHAH'

@app.route('/tests')
def request_speed_tests():
	db = get_db()
	cursor = db.execute('select * from tests;')
	tests  = cursor.fetchall()
	return render_template('index.html',tests=tests)	

#To set to a specific ip app.run(host="192.168.1.7",port=5010) handy if your pc has a few ip's
if __name__ == '__main__':
	app.run(host="192.168.0.39", port = 5000)
