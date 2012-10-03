Reseau
======

Let's see what we'll end up getting here.


Installation
============

Reseau is [Flask](http://flask.pocoo.org/)-powered, which means that you'll need to install Flask, duh:

    easy_install Flask

What was so hard about this?

To initalize the database, fire up a python shell and:

    from reseau import init_db
    init_db()

If no exceptions are thrown, it might have worked. Whatever that means.


Running
=======

Execute

    python reseau.py
