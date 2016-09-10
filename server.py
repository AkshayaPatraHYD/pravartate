# all the imports
import os,binascii
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, Blueprint
from flaskext.mysql import MySQL
from config import config
import datetime
import chartkick
 
import logging
credentials = None

mysql = MySQL()
# create our little application :)

app = Flask(__name__)

for key in config:
    app.config[key] = config[key]

mysql.init_app(app)
app.config.from_object(__name__)

ck = Blueprint('ck_page', __name__, static_folder=chartkick.js(), static_url_path='/static')
app.register_blueprint(ck, url_prefix='/ck')
app.jinja_env.add_extension("chartkick.ext.charts")

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

# Methods and routes

@app.route('/')
def screen():
    return render_template('index.djt')

@app.route('/chart')
def chart():
    data = {'Chrome': 52.9, 'Opera': 1.6, 'Firefox': 27.7}
    return render_template('charts.djt', data=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    global store
    error = None
    db = get_cursor()
    session['temp'] = 0
    if request.method == 'POST':
        email = str(request.form['email'])
        pwd = str(request.form['password'])
        sql = 'select count(*) from Login where email="%s" and password=MD5("%s")'%(email, pwd)
        db.execute(sql)
        data = db.fetchone()[0]
        if not data:
            error = 'Invalid Credentials'
        else:
            getId = 'select loginId from Login where email="%s" and password=MD5("%s")'%(email, pwd)
            db.execute(getId)
            uid = db.fetchone()[0]
            session['logged_in'] = True
            app.config['USERNAME'] = email
            app.config['USERID'] = uid
            db.execute("COMMIT")
            return redirect(url_for('dashboard'))
    return render_template('login.djt', error=error)

@app.route('/kitchen', methods=['GET', 'POST'])
def insertkitchen():
    db = get_cursor()
    if request.method == 'POST':
        tempqry='select count(*) from Kitchen'
        db.execute(tempqry)
        idnum = db.fetchone()[0]+1
        kcode = str(request.form['kcode'])
        kname = str(request.form['kname'])
        area = str(request.form['area'])
        mid = int(request.form['mid'])
        dist = str(request.form['dist'])
        city = str(request.form['city'])
        setkitchen = 'insert into Kitchen values("%d","%s","%s","%s","%d","%s","%s")'%(idnum,kcode,kname,area,mid,dist,city)
        db.execute(setkitchen)
        db.execute("COMMIT")
        return redirect(url_for('insertkitchen'))
    getKitchen='select * from Kitchen'
    db.execute(getKitchen)
    kitchenData=db.fetchall()
    db.execute("COMMIT")
    return render_template('kitchen.djt',data=kitchenData)
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.djt')

if __name__ == '__main__':
    app.debug = True
    app.secret_key=os.urandom(24)
    # app.permanent_session_lifetime = datetime.timedelta(seconds=200)
    app.run(host='0.0.0.0')