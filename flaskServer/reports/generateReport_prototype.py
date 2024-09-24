# xlsxTest - EELE488 Prototype
# Sam Lovering
# Last Updated 09/19/2024 -Drew Currie
#
# This program receives a JSON string from either initData.py or the DB, then converts
# it into a spreadsheet.

# 09/19/2024 Update: Updated from relative to absolute file pathing for the sys.path.insert. The relative pathing seems 
# to break on the RaspberryPi. The cause is not known but the absolute pathing is a temporary fix. 


import datetime
import xlsxwriter
import json
import sys

#For some reason the relative pathing break the pathing on the Pi. Absolute pathing works.
sys.path.insert(0,'/home/55ATAT/55ATAT')
sys.path.insert(0,'/home/55ATAT/55ATAT/APIFuncs')
print(sys.path)
from APIFuncs import utils

def create_spreadsheet(jsonDict):
    #Initialize Spreadsheet

    #Create Excel file with meta data
    fileName = 'attendanceReport' + datetime.datetime.now().strftime("%m%d%H%M") + '.xlsx'

    print("Creating Symbolic Spreadsheet")
    workbook = xlsxwriter.Workbook('xlsx/'+fileName)
    worksheet = workbook.add_worksheet()

    #Turn Timestamp into a "P", create note of timestamp
    designation_format = workbook.add_format({'bold': True, 'bg_color': '#D47554', 'align': 'center'})

    #Create Header for file
    colIterator = 1  #Temp colIterator
    headerKeys = jsonDict[0].keys()
    for key in headerKeys:
        worksheet.write(0, colIterator, key)
        colIterator += 1


    #Start Iterators at 0 (Temp, rework with yields)
    rowIterator = 1
    colIterator = 1
    #Write Data to spreadsheet
    for i in jsonDict:
        worksheet.write(rowIterator, 0, int(jsonDict.index(i)))
        for bodyKey, bodyVal in i.items():
            if bodyKey == 'Timestamp':
                worksheet.write(rowIterator, colIterator, 'P', designation_format)
                worksheet.write_comment(rowIterator, colIterator, str(bodyVal))
            else:
                worksheet.write(rowIterator, colIterator, str(bodyVal))
            colIterator += 1
        rowIterator += 1
        colIterator = 1
    worksheet.autofit()
    worksheet.set_column_pixels('E:E', 100)
    workbook.close()

    return fileName

#This function parses TestJSON into readable data for spreadsheet.
def parse_attendance_events():
    oneWeekAgo = datetime.datetime.now() - datetime.timedelta(days=7)
    utils.GetAttendanceReport(oneWeekAgo, 'attendanceReport.json')
    f = open('attendanceReport.json')
    events = f.read().strip()
    events = '[' + events + ']'
    events = events.replace('}{', '},{')
    data = json.loads(events)
    print(data)
    return data


#This function does JSON handling for create_spreadsheet
def generate_spreadsheet():
    fileName = create_spreadsheet(parse_attendance_events())
    return json.dumps(fileName)


if __name__ == "__main__":
    print("xlsxTest called with __main__")
    generate_spreadsheet()
