# imports
import datetime
import slugify
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from flaskext.mongoengine import MongoEngine
from flaskext.markdown import Markdown
from flaskext.debugtoolbar import DebugToolbarExtension

# application
app = Flask(__name__)
app.config.from_pyfile('config.default.py', silent=True)
app.config.from_pyfile('config.py', silent=True)
db = MongoEngine(app)
Markdown(app)
toolbar = DebugToolbarExtension(app)


# comments
class Comment(db.EmbeddedDocument):
    content = db.StringField()
    name = db.StringField(max_length=120)
    email = db.StringField(max_length=255)
    published_date = db.DateTimeField(default=datetime.datetime.now)

# posts
class Post(db.Document):
    title = db.StringField(max_length=120, required=True)
    #author = ReferenceField(User)
    tags = db.ListField(db.StringField(max_length=50))
    comments = db.ListField(db.EmbeddedDocumentField(Comment))
    published_date = db.DateTimeField(default=datetime.datetime.now)
    slug = db.StringField(max_length=120)
    type = 'post'
    meta = {'allow_inheritance': True}

class TextPost(Post):
    content = db.StringField()
    type = 'text'

#class ImagePost(Post):
#    image_path = db.StringField()

class LinkPost(Post):
    url = db.StringField(required=True)
    type = 'link'

# routing
@app.route('/')
def show_homepage():
    posts = Post.objects.order_by("-published_date")
    return render_template(app.config['TPL_DIR'] + '/show_homepage.html',posts=posts)

#@app.route('/post/<post_slug>')

@app.route('/add', methods=['POST'])
def add_post():
    if not session.get('logged_in'):
        abort(401)
    if request.form['type'] == 'text':
        new_post = TextPost(title=request.form['title'], content=request.form['content'])
    elif request.form['type'] == 'link':
        new_post = LinkPost(title=request.form['title'], url=request.form['content'])
    else:
        new_post = Post(title=request.form['title'])
    new_post.slug = slugify.slugify(request.form['title'])
    new_post.tags = map(lambda x:x.strip(), request.form['tags'].split(','))
    new_post.save()
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

