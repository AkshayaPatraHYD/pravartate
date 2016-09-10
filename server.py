# all the imports
import os,binascii
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flaskext.mysql import MySQL
from config import config
import datetime
 
import logging
credentials = None

mysql = MySQL()
# create our little application :)

app = Flask(__name__)

for key in config:
    app.config[key] = config[key]

mysql.init_app(app)
app.config.from_object(__name__)

def tup2float(tup):
    return float('.'.join(str(x) for x in tup))

def get_cursor():
    return mysql.connect().cursor()

@app.teardown_appcontext
def close_db(self):
    """Closes the database again at the end of the request."""
    get_cursor().close()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.djt'), 404

@app.route('/')
def screen():
    return render_template('index.djt')

if __name__ == '__main__':
    app.debug = True
    app.secret_key=os.urandom(24)
    # app.permanent_session_lifetime = datetime.timedelta(seconds=200)
    app.run(host='0.0.0.0')