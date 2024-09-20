from flask import Flask, Blueprint, render_template, send_from_directory, request, jsonify, make_response
from flask_cors import CORS
from reports import generateReport
from APIFuncs import utils
from APIFuncs import MariaDBapi
import sys
import os
import time
app = Flask(__name__)
CORS(app)

sys.path.append(os.path.join(sys.path[0], '/xlsx'))

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
    dir = 'flaskServer/xlsx/'
    print(dir+fileName)
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

@app.route('/api/getRoles',methods=['GET'])
def getRoles():
    return make_response(jsonify(utils.getRoles()), 200)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    print("Flask Server started from app.py")
    app.run(host='0.0.0.0', port=5000, debug=True)
