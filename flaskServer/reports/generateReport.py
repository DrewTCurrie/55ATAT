# xlsxTest - EELE488 Prototype
# Sam Lovering
# Last Updated 5/12/2024
#
# This program receives a JSON string from either initData.py or the DB, then converts
# it into a spreadsheet.

import datetime
import os

import sqlalchemy
import xlsxwriter
import json
import sys

from sqlalchemy import and_, select
from sqlalchemy.orm import declarative_base

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'APIFuncs')))
from APIFuncs import utils
from APIFuncs import MariaDBapi as api

def create_spreadsheet(jsonDict):
    #Initialize Spreadsheet

    #Create Excel file with meta data
    fileName = 'attendanceReport' + datetime.datetime.now().strftime("%m%d%H%M") + '.xlsx'

    print("Creating Symbolic Spreadsheet")
    workbook = xlsxwriter.Workbook('xlsx/' + fileName)
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
    #utils.GetAttendanceReport(oneWeekAgo, 'attendanceReport.json')
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


# This function creates a database query based on optional params passed by reportModal web component.
def filter_events(name=None, role=None, start_time=None, end_time=None):
    #Create Session (TODO: move this to a singular session for the codebase)
    #api.Base.metadata.create_all(api.engine)
    Session = sqlalchemy.orm.sessionmaker()
    Session.configure(bind=api.engine)
    Session = Session()

    #Initalize Query
    query = Session.query(api.AttendanceEvent)

    #Create Filters
    filters = []
    if name:
        filters.append(api.AttendanceEvent.AttendeeInitials == name)
    if role: #TODO I forgot about how the db handles roles, I gotta revise this section.
        query = Session.query(api.AttendanceEvent, api.Attendee)
    if start_time is not None:
        filters.append(api.AttendanceEvent.Timestamp >= start_time)
    else:
        filters.append(api.AttendanceEvent.Timestamp >= (datetime.datetime.now() - datetime.timedelta(days=7)))

    if end_time is not None:
        filters.append(api.AttendanceEvent.Timestamp <= end_time)
    else:
        filters.append(api.AttendanceEvent.Timestamp <= datetime.datetime.now())
    #Write filters to query
    query = query.filter(and_(*filters))

    results = query.all()
    for event in results:
        print(event.AttendeeInitials)

    return query.all()


if __name__ == "__main__":
    print("xlsxTest called with __main__")
    filter_events(end_time=datetime.datetime.now(),start_time=(datetime.datetime.now() - datetime.timedelta(days=7)))
    #generate_spreadsheet()
