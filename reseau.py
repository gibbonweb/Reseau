# imports
from __future__ import with_statement
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

# default configuration
DATABASE = '/tmp/reseau.db'
DEBUG = True
SECRET_KEY = 'ThisReseauIsAwesome'
USERNAME = 'admin'
PASSWORD = 'default'

# application
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('RESEAU_SETTINGS', silent=True)

# DB handling
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

# routing
@app.route('/')
def show_homepage():
    return "Reseau!"

# run
if __name__ == '__main__':
    app.run()

