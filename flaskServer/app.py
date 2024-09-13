from flask import Flask, Blueprint, render_template, send_from_directory, request, jsonify, make_response
from flask_cors import CORS
from reports import generateReport
from APIFuncs import utils
app = Flask(__name__)
CORS(app)


@app.route('/api/generateReport', methods=['GET', 'POST'])
def generate_report():
    data = request.json
    name = data.get('name')
    role = data.get('role')
    start_date = data.get('startDate')
    end_date = data.get('endDate')
    print(end_date)
    fileName = generateReport.generate_spreadsheet(name, role, start_date, end_date)
    return make_response(jsonify(fileName, success=True), 200)

@app.route('/api/download/<path:filename>', methods=['GET', 'POST'])
def download_file(filename):
    return send_from_directory(directory='xlsx', path=filename, as_attachment=True)

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
