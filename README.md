Reseau
======

Let's see what we'll end up getting here.


Installation
============

Reseau is [Flask](http://flask.pocoo.org/)-powered, which means that you'll need the following:
    
    cd <your webserver root>
    git clone git://github.com/gibbonweb/Reseau.git <websitename>
    cd <websitename>
    sudo apt-get install python-virtualenv
    virtualenv venv
    . venv/bin/activate
    pip install Flask
    pip install Flask-Markdown
    pip install https://github.com/sbook/flask-mongoengine/tarball/master
    pip install slugify
    pip install https://github.com/sbook/flask-debugtoolbar/tarball/master


Running
=======

## Development:

    python runserver.py

## Production:

uWSGI recommended.
