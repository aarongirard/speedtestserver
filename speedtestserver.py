import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
	render_template, flash

#create the application
app = Flask(__name__)


