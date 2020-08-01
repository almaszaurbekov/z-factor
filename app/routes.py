from flask import render_template, flash, redirect
from app import app
from app.functions import *

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Index')