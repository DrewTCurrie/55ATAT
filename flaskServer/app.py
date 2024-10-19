import datetime
import json
import uuid

from flask import Flask, Blueprint, render_template, send_from_directory, request, jsonify, make_response, send_file
from flask_cors import CORS
from flask_jwt_extended import create_access_token, JWTManager

from reports import generateReport, reportScheduler
from APIFuncs import utils
from APIFuncs import MariaDBapi
from APIFuncs import badgeGenerator
from APIFuncs import auth
from APIFuncs import messages
import sys
import os
import time

#Scheduling library
import schedule
#Need threading for schedules
from threading import Thread

#Initialize Flask App
app = Flask(__name__)

#Cross Origin Configuratoin
#CORS(app,resources={r"*": {"origins":"http://localhost:5173"""}})
CORS(app)

#JWT Configuration (For session tokens)
app.config['JWT_SECRET_KEY'] = 'faf4f00ab5cdc4b33e197d879118da6730cb7d9bd71cfdff253f9772e346465313daf5dc6f744ae5de5d9dc77142808cad673cfeab879c2b7d7e7ccaff0fc43a'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=12)  #12 hours before relogin.
jwt = JWTManager(app)

#Add Pathing for external folders
sys.path.append(os.path.join(sys.path[0], '/xlsx'))
sys.path.append(os.path.join(sys.path[0], '/profileImage'))
image_folder = 'flaskServer/profileImage'


#--Schedule funciton. Needs to stay in the main flask app ----------------------------------------------
def ScheduleManager():
    while 1:
        schedule.run_pending()
        time.sleep(5)


#----------Web Routes ------------------------------------------------------------------------------------


#----------Report Routes ---------------------------------------------------------------------------------
@app.route('/api/generateReport', methods=['GET', 'POST'])
def generate_report():
    data = request.json
    name = data.get('name')
    role = data.get('role')
    start_date = data.get('startDate')
    end_date = data.get('endDate')
    fileName = generateReport.generate_spreadsheet(name, role, start_date, end_date)
    #Checking if file exists for a minute before throwing an error.
    start_time = time.time()
    while time.time() - start_time < 60:
        if os.path.isfile('/home/55ATAT/55ATAT/flaskServer/xlsx/' + fileName):
            print('found file')
            return make_response(jsonify(fileName), 200)
        time.sleep(1)
    return make_response("Error: File not found", 404)


@app.route('/api/download/<path:filename>', methods=['GET', 'POST'])
def download_file(filename):
    print("filename received: " + filename)
    return send_from_directory(directory='xlsx', path=filename, as_attachment=True)


#--------------- Getter Routes -----------------------------------------------------
@app.route('/api/attendeeInitials', methods=['GET'])
def getAttendeeInitials():
    return make_response(utils.getAllUserInitials(), 200)


@app.route('/api/getRoles', methods=['GET'])
def getRoles():
    return make_response(jsonify(utils.getRoles()), 200)


@app.route('/api/getAllAttendees', methods=['GET'])
def getAllAttendees():
    return make_response(jsonify(utils.getAllAttendees()), 200)

@app.route('/api/getAttendeeInitialsAndID', methods=['GET'])
def getAttendeeInitialsAndID():
    return make_response(jsonify(utils.getAllAttendeeInitialsAndIDs()),200)

#This endpoint returns the 50 most recent attendance events for usage in the webpage table. This can be expanded based on testing.
@app.route('/api/getRecentEvents', methods=['GET'])
def getRecentEvents():
    return make_response(jsonify(utils.getEvents(50)), 200)


#This endpoint takes a userID, and creates an attendance event with it
@app.route('/api/scanEvent', methods=['POST'])
def scanEvent():
    data = request.json
    response = utils.NewAttendanceEvent(data.get('id'))
    if response is False:
        return make_response(jsonify({'message': "Unable to find attendee: " + data.get('id')}), 400)
    else:
        return make_response(jsonify({'message': "Event Created for attendee: " + data.get('id')}), 200)


#createAccount parses the formdata, creates an account, saves an image associated with the id for badge creation, and returns the id.
@app.route('/api/createAccount', methods=['POST'])
def createAccount():
    #Parse form data for username and roles
    newAccount = {
        "Client": False,
        "Employee": False,
        "ABA_Earlychildhood": False,
        "ABA_Teen": False,
        "Occupational_Therapy": False,
        "Speech_Therapy": False,
        "Administrator": False,
        "Employee_SPOT": False,
        "Employee_BCBA": False,
        "Employee_RBT": False,
        "Employee_Other": False,
        "AttendeeInitials": ' '
    }
    #Assigning Roles to newAccount
    for role in json.loads(request.form['roles']):
        if role in newAccount.keys():
            newAccount[role] = True

    #Assigning initials to a new account
    newAccount['AttendeeInitials'] = request.form['name']

    #Creating a new Account with initals and roles
    UserID = utils.NewAttendeeFromWeb(newAccount)

    #Saving Image (For usage in creating QR Code)
    if 'file' in request.files:
        image = request.files['file']
        # Create file name with UserID
        file_extension = '.png'  # Get the file extension
        new_filename = f"{UserID}{file_extension}"
        save_path = os.path.join(image_folder, new_filename)
        with open(save_path, 'wb') as f:
            f.write(image.read())
    return make_response(jsonify(UserID), 200)


@app.route('/api/generateBadge', methods=['POST'])
def generateQR():
    # Get Data for UserID
    data = request.json
    # Call generate_badge, which will create a badge and URL for it.
    badgeURL = badgeGenerator.generate_badge(data.get('userID'))
    return make_response(badgeURL, 200)


@app.route('/api/createAdmin', methods=['POST'])
def createAdministrator():
    # Parse JSON Data
    data = request.json
    newAdministrator = {
        "ID": data.get('adminID'),
        'username': data.get('username'),
        'password': data.get('password')
    }
    # call createAdministrator to add to DB
    utils.createAdministrator(newAdministrator)
    return make_response(jsonify({"message": "Success"}), 200)


#createEvent will be called if an Attendance Event is create from the webpage.
@app.route('/api/createEvent', methods=['POST'])
def createEvent():
    # Parse JSON Data
    data = request.json
    #A lot of null checks happen with this feature, so data is passed directly to the utils
    utils.createEventFromWeb(data)
    return make_response(jsonify({"message": "Success"}), 200)


@app.route('/api/deleteEvent', methods=['POST'])
def deleteEvent():
    data = request.json
    utils.deleteEvent(data.get('ID'))
    return make_response(jsonify({"message": "Success"}), 200)


@app.route('/api/editEvent', methods=['POST'])
def editEvent():
    data = request.json
    utils.editEvent(data)
    return make_response(jsonify({"message": "Success"}), 200)


#editAccount recieves a formdata object from the front end, then updates the db data with it.
@app.route('/api/editAccount', methods=['POST'])
def editAccount():
    accountDetails = {
        "Client": False,
        "Employee": False,
        "ABA_Earlychildhood": False,
        "ABA_Teen": False,
        "Occupational_Therapy": False,
        "Speech_Therapy": False,
        "Administrator": False,
        "Employee_SPOT": False,
        "Employee_BCBA": False,
        "Employee_RBT": False,
        "Employee_Other": False,
        "AttendeeInitials": ' ',
        "ID": '',
    }

    #Assigning Roles to newAccount
    for role in json.loads(request.form['roles']):
        if role in accountDetails.keys():
            accountDetails[role] = True

    #Assigning initials to a new account
    accountDetails['AttendeeInitials'] = request.form['name']
    #Assigning ID to a new account
    accountDetails['ID'] = request.form['id']

    #Saving Image (For usage in creating QR Code)
    if 'file' in request.files:
        image = request.files['file']
        # Create file name with UserID
        file_extension = '.png'  # Get the file extension
        new_filename = f"{request.form['id']}{file_extension}"
        save_path = os.path.join(image_folder, new_filename)
        with open(save_path, 'wb') as f:
            f.write(image.read())

    utils.editAttendeeFromWeb(accountDetails)
    return make_response(jsonify({"message": "Success"}), 200)


#If the account being edited is an admin and there is new content, edit the admin.
@app.route('/api/editAdmin', methods=['POST'])
def editAdmin():
    # Parse JSON Data
    data = request.json
    newAdministrator = {
        "ID": data.get('adminID'),
        'UserName': data.get('username'),
        'Password': data.get('password')
    }
    # call createAdministrator to add to DB
    utils.editAdministrator(newAdministrator)
    return make_response(jsonify({"message": "Success"}), 200)


@app.route('/api/deleteAccount', methods=['POST'])
def deleteAccount():
    #Parse JSON Data
    data = request.json
    utils.deleteAttendee(data.get('ID'))
    return make_response(jsonify({"message": "Success"}), 200)


# -------------- Authentication Routes ------------------------------------------
@app.route('/api/login', methods=['POST'])
def login():
    #Parse JSON data
    loginData = request.json
    loginResponse = auth.attemptLogin(loginData.get('UserName'), loginData.get('Password'))
    if loginResponse.get('Success') == True:
        #Create User Token
        userToken = create_access_token(identity=loginData.get('UserName'))
        loginResponse['userToken'] = userToken
        return make_response(jsonify(loginResponse)), 200
    else:
        return make_response(jsonify(loginResponse), 401)


#--------------- Settings Routes -----------------------------------------------------

#---------------Default Messages Routes -----------------------------------------------------
@app.route('/api/getDefaultMessage',methods=['GET'])
def getDefaultMessage():
    defaultMessage = messages.getDefaultMessage()
    return make_response(jsonify({"message": defaultMessage}), 200)
# @app.route('/api/getDefaultAudio',methods=['GET'])
# def getDefaultAudio():

@app.route('/api/setDefaultMessage', methods=['POST'])
def setDefaultMessage():
    #Parse JSON data
    data = request.json
    messages.setDefaultMessage(data.get('message'))
    return make_response(jsonify({"message": "Success"}), 200)

@app.route('/api/resetDefaults', methods=['GET'])
def resetDefault():
    messages.resetDefaults()
    return make_response(jsonify({"message": "Success"}), 200)

#---------------Default Audio Routes -----------------------------------------------------

@app.route('/api/setDefaultAudio',methods=['POST'])
def setDefaultAudio():
    #This will be passed in as a form data.
    messages.setDefaultAudio(request.files['audio'])
    return make_response(jsonify({"message": "Success"}), 200)

@app.route('/api/getDefaultAudio',methods=['GET'])
def getDefaultAudio():
    audioURL = messages.getDefaultSuccessAudio()
    return make_response(jsonify({"url": audioURL}), 200)

@app.route('/api/getFailureAudio', methods=['GET'])
def getFailureAudio():
    audioURL = messages.getFailureAudio()
    return make_response(jsonify({"url": audioURL}), 200)

#---------------Attendee Messages Routes -----------------------------------------------------
@app.route('/api/getAttendeeMessage',methods=['POST'])
def getAttendeeMessage():
    # Parse JSON data
    data = request.json
    #Get Attendee Message from messages.py
    message = messages.getAttendeeMessage(data.get('id'))
    return make_response(jsonify({"message": message}), 200)

@app.route('/api/setAttendeeMessage', methods=['POST'])
def setAttendeeMessage():
    data = request.json
    messages.setAttendeeMessage(data.get('id'),data.get('message'))
    return make_response(jsonify({"message": "Success"}), 200)

@app.route('/api/resetAttendee', methods=['POST'])
def resetAttendee():
    data = request.json
    messages.resetAttendee(data.get('id'))
    return make_response(jsonify({"message": "Success"}), 200)

#---------------Attendee Audio Routes -----------------------------------------------------
@app.route('/api/getAttendeeAudio', methods=['POST'])
def getAttendeeAudio():
    data = request.json
    audioURL = messages.getAttendeeAudio(data.get('id'))
    return make_response(jsonify({"url": audioURL}), 200)

@app.route('/api/setAttendeeAudio',methods=['POST'])
def setAttendeeAudio():
    #This will be passed in as a form data.
    messages.setAttendeeAudio(request.form['id'],request.files['audio'])
    return make_response(jsonify({"message": "Success"}), 200)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    print("Flask Server started from app.py")
    #---------Scheduled Processes-----------------------------------------------------------------------------
    schedule.every().day.at("21:00").do(reportScheduler.CheckReportsSchedule)
    #schedule.every(60).seconds.do(reportScheduler.CheckReportsSchedule)

    #This may not be the most effecient way to run this code however I cannot find a more effecient way to run 
    #python code on a monthly basis. This seems to work but it does require a thread that is running that is basically
    #just polling the current date/time every 15 minutes to see if it is the correct time to generate a report
    #It is more effecient than the original polling of like every second
    ScheduleMangerThread = Thread(target=ScheduleManager)
    ScheduleMangerThread.start()
    app.run(host='0.0.0.0', port=5000, debug=False)
