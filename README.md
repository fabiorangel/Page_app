Page App was developed using a Python Framework called: web2py.

The application is working on the url: fabiorangel.com:8000/Page_app

::Choice of Technologies::

-Python: I like to develop in Python. It's a particular choice of language. Moreover, Python is faster developed than Java.
-web2py: Easy install framework with faster results (easy to integrate with MongoDB, a useful database when developing apps with tweets, not used in this work).
-Oauth2: The requests to fetch tweets is implemented in Python using Oauth2 lib.
-Google Maps: map implemented with javascript on frontend.
-DBPedia Lookup: using DBpedia lookup to get place description.

::Structure (development)::

Web2py is MVC framework

-Controller: https://github.com/fabiorangel/Page_app/blob/master/applications/Page_app/controllers/default.py

Backend part.

1) get info from form
2) get map position from google maps
3) get 5 tweets
4) get Brief Description from DBPedia

Return all information on a Dictionary

-View: https://github.com/fabiorangel/Page_app/blob/master/applications/Page_app/views/default/index.html

Frontend part.

1) Form
2) Map Canvas
3) Tweets
4) Brief Description

CSS: https://github.com/fabiorangel/Page_app/blob/master/applications/Page_app/static/css/page_app.css

How to run locally (if need):

git clone https://github.com/fabiorangel/Page_app.git
apt-get install python2.7
apt-get install python-pip
pip install oauth2

running:

python web2py.py -a "{PASSWORD}" -i 127.0.0.1 -p 8000

accessing url: localhost:8000/Page_app
