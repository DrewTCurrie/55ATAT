from flask import Flask, Blueprint, render_template, send_from_directory, request, jsonify, make_response
from flask_cors import CORS
from reports import generateReport

app = Flask(__name__)
CORS(app)


@app.route('/api/generateReport', methods=['GET', 'POST'])
def generate_report():
    print(request.data)
    fileName = generateReport.generate_spreadsheet()
    #return fileName
    return make_response(jsonify(success=True), 201)

@app.route('/api/download/<path:filename>', methods=['GET', 'POST'])
def download_file(filename):
    return send_from_directory(directory='xlsx', path=filename, as_attachment=True)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    print("Flask Server started from app.py")
    app.run(host='0.0.0.0', port=5000, debug=True)
