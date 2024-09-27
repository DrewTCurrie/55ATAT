import json

from flask import Flask, Blueprint, render_template, send_from_directory, request, jsonify, make_response, send_file
from flask_cors import CORS
from reports import generateReport
from APIFuncs import utils
from APIFuncs import MariaDBapi
from APIFuncs import badgeGenerator
import sys
import os
import time

app = Flask(__name__)
CORS(app,resources={r"*": {"origins":"http://localhost:5173"""}})

sys.path.append(os.path.join(sys.path[0], '/xlsx'))
sys.path.append(os.path.join(sys.path[0], '/profileImage'))
image_folder = 'flaskServer/profileImage'


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
        if os.path.isfile('/home/55ATAT/55ATAT/flaskServer/xlsx/'+fileName):
            print('found file')
            return make_response(jsonify(dir + fileName), 200)
        time.sleep(1)
    return make_response("Error: File not found", 404)


@app.route('/api/download/<path:filename>', methods=['GET', 'POST'])
def download_file(filename):
    print("filename received: " + filename)
    modifiedPath = filename[17:]
    print("ModifiedPath is: " + modifiedPath)
    return send_from_directory(directory='xlsx', path = modifiedPath, as_attachment=True)

@app.route('/api/attendeeInitials',methods=['GET'])
def getAttendeeInitials():
    return make_response(utils.getAllUserInitials(), 200)


@app.route('/api/getRoles', methods=['GET'])
def getRoles():
    return make_response(jsonify(utils.getRoles()), 200)

@app.route('/api/getAllAttendees' , methods=['GET'])
def getAllAttendees():
   return make_response(jsonify(utils.getAllAttendees()), 200)


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

#editAccount recieves a formdata object from the front end, then updates the db data with it.
@app.route('/api/editAccount',methods=['POST'])
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

@app.route('/api/deleteAccount',methods=['POST'])
def deleteAccount():
    #Parse JSON Data
    data = request.json
    utils.deleteAttendee(data.get('ID'))
    return make_response(jsonify({"message": "Success"}), 200)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    print("Flask Server started from app.py")
    app.run(host='0.0.0.0', port=5000, debug=True)
