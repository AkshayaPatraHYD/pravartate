# all the imports
import os,binascii
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, Blueprint
from flaskext.mysql import MySQL
from config import config
import datetime
import chartkick
import json
 
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
#Logout 
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return render_template('index.djt')

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

@app.route('/school', methods=['GET', 'POST'])
def insertSchool():
    db = get_cursor()
    if request.method == 'POST':
        tempqry = 'select count(*) from School'
        db.execute(tempqry)
        schoolid = db.fetchone()[0]+1
        # Parameters from form
        schoolName = str(request.form['schoolName'])
        schoolMandal = str(request.form['mandal'])
        schoolDistrict = str(request.form['district'])
        ItoVAttendance = int(request.form['ItoVTotal'])
        VItoVIIIAttendance = int(request.form['VItoVIIITotal'])
        IXtoXAttendance = int(request.form['IXtoXTotal'])
        # latitude = str(request.form['latitude'])
        # longitude = str(request.form['longitude'])
        # @todo: Make them come somehow from a map.
        latitude = 17.772928
        longitude = 78.289101
        schoolAdminName = str(request.form['schoolPrincipalName'])
        schoolAdminPhone = str(request.form['schoolAdminPhone'])
        schoolAdminDesig = str(request.form['schoolAdminDesignation'])
        # End of parameters from form
        schoolAdminTemp = 'select count(*) from SchoolAdmins'
        db.execute(schoolAdminTemp)
        adminid = db.fetchone()[0]+1
        # All the required values are here from UI and DB Pre-requisites
        # Computations and DB Results of processing
        totalAttendance = ItoVAttendance + VItoVIIIAttendance + IXtoXAttendance
        # School Inserts
        setSchool = 'insert into School values("%d","%s","%s","%s","%d","%d","%d","%d","%f","%f")'
        db.execute(setSchool%(schoolid, schoolDistrict, schoolName, schoolMandal, ItoVAttendance, VItoVIIIAttendance, IXtoXAttendance, totalAttendance, latitude, longitude))
        # SchoolAdmin Inserts
        setSchoolAdmins = 'insert into SchoolAdmins values("%d","%d","%s","%s","%s")'
        db.execute(setSchoolAdmins%(schoolid, adminid, schoolAdminName, schoolAdminPhone, schoolAdminDesig))
        db.execute("COMMIT")
        return redirect(url_for('insertSchool'))
    getSchools = 'select * from School'
    db.execute(getSchools)
    schoolData = db.fetchall()
    db.execute("COMMIT")
    return render_template('school.djt', data=schoolData)

# API Controllers
# API To register the attendance
# To register 1 SMS Detail
# Example usage for 1 single SMS Registration
# 1. /api/todaysAttendance/1234567890/22,14,18
@app.route('/api/todaysAttendance/<phoneNumber>/<text>', methods=['GET', 'POST'])
def registerTodaysAttendance(phoneNumber=None, text=None):
    db = get_cursor()
    givenPhoneNumber = str(phoneNumber)
    givenTextMessage = str(text)
    attendanceDetails = givenTextMessage.split(',')
    attendanceItems = len(attendanceDetails)
    params = {}
    if (attendanceItems == 1):
        ItoVAttendance = int(attendanceDetails[0])
        VItoVIIIAttendance = 0
        IXtoXAttendance = 0
    elif (attendanceItems == 2):
        ItoVAttendance = int(attendanceDetails[0])
        VItoVIIIAttendance = int(attendanceDetails[1])
        IXtoXAttendance = 0
    else:
        ItoVAttendance = int(attendanceDetails[0])
        VItoVIIIAttendance = int(attendanceDetails[1])
        IXtoXAttendance = int(attendanceDetails[2])
    getAdminDetails = 'select * from SchoolAdmins where adminPhoneNumber="%s"'%givenPhoneNumber
    db.execute(getAdminDetails)
    adminFetchedDetails = db.fetchone()
    schoolid = adminFetchedDetails[0]
    adminid = adminFetchedDetails[1]
    adminName = adminFetchedDetails[2]
    if schoolid:
        # Given the school id map it to the school and fetch the required details
        schoolQuery = 'select * from School where schoolid="%d"'%schoolid
        db.execute(schoolQuery)
        schoolData = db.fetchall()[0]
        if schoolData:
            mandal = schoolData[3]
            schoolTotal = int(schoolData[7])
            schoolName = schoolData[2]
            timestampdata = datetime.datetime.now().strftime("%d/%m/%y %H:%M")
            attendanceInsert = 'insert into AttendanceOLTP values("%s","%s","%s","%d","%d","%s","%d","%s","%s","%d","%d","%d")'
            db.execute(attendanceInsert%(timestampdata, phoneNumber, text, schoolid, adminid, adminName, schoolTotal, schoolName, mandal, ItoVAttendance, VItoVIIIAttendance, IXtoXAttendance))
            db.execute("COMMIT")
            params['success'] = 'Successfully recorded attendance'
            params['schoolName'] = schoolName
            params['phoneNumber'] = phoneNumber
            params['primaryItoV'] = ItoVAttendance
            params['middleVItoVIII'] = VItoVIIIAttendance
            params['highIXtoX'] = IXtoXAttendance
            return json.dumps(params)
    params['error'] = 'Error, Please check again and follow format /api/todaysAttendance/1234567890/22,14,18'
    return json.dumps(params)

@app.route('/visualize')
def visualize():
    db = get_cursor()
    sql = 'select * from AttendanceOLTP'
    db.execute(sql)
    OLTPData = db.fetchall()
    return render_template('visualize.djt', data = OLTPData)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.djt')

if __name__ == '__main__':
    app.debug = True
    app.secret_key=os.urandom(24)
    # app.permanent_session_lifetime = datetime.timedelta(seconds=200)
    app.run(host='0.0.0.0')