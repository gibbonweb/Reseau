# imports
from __future__ import with_statement
import pymongo
import datetime
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from flaskext.markdown import Markdown

# application
app = Flask(__name__)
app.config.from_pyfile('config.default.py', silent=True)
app.config.from_pyfile('config.py', silent=True)
Markdown(app)

# DB handling
def connect_db():
    return pymongo.MongoClient('localhost', 27017)

@app.before_request
def before_request():
    g.dbconn = connect_db()
    g.db = g.dbconn.local

@app.teardown_request
def teardown_request(exception):
    g.dbconn.close()

# routing
@app.route('/')
def show_homepage():
    reseau = g.db.reseau
    posts = reseau.find().sort('date',pymongo.DESCENDING)
    return render_template('show_homepage.html',posts=posts)

@app.route('/add', methods=['POST'])
def add_post():
    if not session.get('logged_in'):
        abort(401)
    post = {"author": "johannes",
            "title": request.form['title'],
            "content": request.form['content'],
            "date": datetime.datetime.utcnow()}
    reseau = g.db.reseau
    post_id = reseau.insert(post)
    if post_id != False:
        flash('New post was successfully posted')
    return redirect(url_for('show_homepage'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_homepage'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_homepage'))

# run
if __name__ == '__main__':
    app.run()

