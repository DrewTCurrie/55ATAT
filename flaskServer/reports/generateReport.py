# generateReport
# Sam Lovering
# Last Updated 9/11/2024
#
# When query params are passed in this program will parse them, query the systems' database
# then create an Excel spreadsheet based on the results.
#
# Big Ticket TODOs:
# 1. Create Aggregate information like in original
# 2. Make iteration not delete from behind
# 3. implement types.
import datetime
import os
import collections
import sqlalchemy
import xlsxwriter
import json
import sys

from sqlalchemy import and_
from sqlalchemy.orm import declarative_base

#This was some chatgpt thing, TODO replace with something more clear.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'APIFuncs')))
from APIFuncs import MariaDBapi as api

class report_params:
    def __init__(self, name=None, start_date=None, end_date=None):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.query_data = ((),)
        self.attendance_data = collections.defaultdict(list)

    # Generates a range of dates using the report params.
    def generate_date_range(self):
        date_list = []
        current_date = self.start_date
        while current_date <= self.end_date:
            date_list.append(current_date)
            current_date += datetime.timedelta(days=1)
        return date_list
    def parse_query(self):
        for event in self.query_data:
            self.attendance_data[event.ID].append(event)

def create_spreadsheet():
    #Initialize Spreadsheet
    #Create Excel file with meta data
    fileName = ('attendanceReport.xlsx') #Temp, TODO replace with metadata.
    print("Creating Symbolic Spreadsheet")
    workbook = xlsxwriter.Workbook(fileName)
    worksheet = workbook.add_worksheet()

    # Header format TODO: make different formatting for days, types and clients columns
    header_format = workbook.add_format({
        'bold': True,
        'font_color': 'black',
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': '#D3D3D3',  # light gray background
        'border': 1
    })
    # Note Format
    note_format = workbook.add_format({
        'italic': True,
        'font_color': 'red',
        'align': 'right',
        'valign': 'top',
        'text_wrap': True
    })
    #Formatting for Individual Dates (TODO Look into Reduced Hrs, Holiday and Not Scheulded?)
    present_format = workbook.add_format({
        'bg_color': '#fdebd7',
        'align': 'center',
        'valign': 'vcenter'
    })
    approved_cancel_format = workbook.add_format({
        'bg_color': '#6db260',
        'align': 'center',
        'valign': 'vcenter'
    })
    tardy_format = workbook.add_format({
        'bg_color': '#f6ab58',
        'align': 'center',
        'valign': 'vcenter'
    })
    unapproved_cancel_format = workbook.add_format({
        'bg_color': '#c00000',
        'align': 'center',
        'valign': 'vcenter'
    })
    incomplete_format = workbook.add_format({
        'bg_color': '#f6ab58',
        'align': 'center',
        'valign': 'vcenter'
    })
    late_pickup_format = workbook.add_format({
        'bg_color': '#f6ab58',
        'align': 'center',
        'valign': 'vcenter'
    })

    # Merge and format the main title
    worksheet.merge_range('C1:R1', 'Peach Tree Client Attendance Tracker', header_format)
    # Absence Type Key section
    worksheet.write('A2', 'Absence Type Key:', workbook.add_format({'bold': True}))
    worksheet.write('A3', 'Warning: Do not insert rows!', workbook.add_format({'font_color': 'red', 'bold': True}))
    # Merge and write the month dynamically based on the start date (you can customize this further)
    worksheet.merge_range('A4:B4', 'Month: {}'.format(params.start_date.strftime('%B %Y')), header_format)

    # Define the absence types and formats
    keys = ['P', 'C', 'T', 'A', 'I', 'L', '#', 'H', 'X']
    key_descriptions = ['Present', 'Approved Cancellation', 'Tardy (by Unit)', 'Unapp. Cancel. (by day)',
                        'Incomp. Session (by Unit)', 'Late Pickup (by Unit)', 'Reduced by PTC (by hour)', 'PTC Holiday',
                        'Not Scheduled']
    colors = ['#F4CCCC', '#D9EAD3', '#F9CB9C', '#E06666', '#C9DAF8', '#FCE5CD', '#FFF2CC', '#D9D2E9', '#EAD1DC']

    for i, (key, desc, color) in enumerate(zip(keys, key_descriptions, colors)):
        #Formatting for Key (Singular Letter)
        format_key = workbook.add_format({
            'bg_color': color,
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'border': 1
        })
        #Formatting for Key description (explanation)
        format_desc = workbook.add_format({
            'bg_color': color,
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True,
            'border': 1,
            'rotation': 90
        })
        #Write starting from C, populating every other.
        worksheet.write(1, (i*2) + 2, key, format_key)
        worksheet.write(2, (i*2) + 2, desc, format_desc)

    # Note section
    worksheet.merge_range('X2:AA4',
                          'Note: \nIf a client’s attendance is close to lower limit, and they have been called off many times, their actual attendance ratio should be calculated manually',
                          note_format)

    #Get Date List from Class
    date_list = params.generate_date_range()
    #TODO: remove weekends.

    # Write days of the week (e.g., Thur, Fri, etc.)
    days_of_week = [date.strftime('%a') for date in date_list]
    worksheet.write_row('C4', days_of_week, header_format)

    # Write the dates (e.g., 1, 2, 3, etc.)
    dates = [date.strftime('%d') for date in date_list]
    worksheet.write_row('C5', dates, header_format)

    #Add Column Headers for "type" and "client"
    worksheet.write('A5', "Type", header_format)
    worksheet.write('B5', "Client", header_format)

    # Adjust column widths
    worksheet.set_column('A:A', 10)
    worksheet.set_column('B:B', 15)
    worksheet.set_column('C:W', 5)

    #Populate with Database Data.
    for index, (attendeeID, events) in enumerate(params.attendance_data.items()):
        #Write Client Information
        worksheet.write(index+5, 0, "TOBEIMPLEMENTED")
        worksheet.write(index+5, 1, events[0].AttendeeInitials)
        #Write Attendance Data
        for event in events:
            #Convert DB Timestamp into Datetime Object
            event_date = event.Timestamp
            #Iterate and add to worksheet. TODO: Need expanded for TAIL, also prevent deletion
            for colIndex, date in enumerate(date_list):
                if event_date.date() == date.date():
                    worksheet.write(index+5, colIndex+2, "P", present_format)

    # Close the workbook
    workbook.close()

    # #Turn Timestamp into a "P", create note of timestamp
    # designation_format = workbook.add_format({'bold': True, 'bg_color': '#D47554', 'align': 'center'})
    #
    # #Create Header for file
    # colIterator = 1  #Temp colIterator
    # headerKeys = jsonDict[0].keys()
    # for key in headerKeys:
    #     worksheet.write(0, colIterator, key)
    #     colIterator += 1
    #
    # #Start Iterators at 0 (Temp, rework with yields)
    # rowIterator = 1
    # colIterator = 1
    # #Write Data to spreadsheet
    # for i in jsonDict:
    #     worksheet.write(rowIterator, 0, int(jsonDict.index(i)))
    #     for bodyKey, bodyVal in i.items():
    #         if bodyKey == 'Timestamp':
    #             worksheet.write(rowIterator, colIterator, 'P', designation_format)
    #             worksheet.write_comment(rowIterator, colIterator, str(bodyVal))
    #         else:
    #             worksheet.write(rowIterator, colIterator, str(bodyVal))
    #         colIterator += 1
    #     rowIterator += 1
    #     colIterator = 1
    # worksheet.autofit()
    # worksheet.set_column_pixels('E:E', 100)
    # workbook.close()
    #
    # return fileName


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
def filter_events(name=None, role=None, start_date=None, end_date=None):
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
    if start_date is not None:
        filters.append(api.AttendanceEvent.Timestamp >= start_date)
    else:
        filters.append(api.AttendanceEvent.Timestamp >= (datetime.datetime.now() - datetime.timedelta(days=7)))

    if end_date is not None:
        filters.append(api.AttendanceEvent.Timestamp <= end_date)
    else:
        filters.append(api.AttendanceEvent.Timestamp <= datetime.datetime.now())
    #Write filters to query
    query = query.filter(and_(*filters))

    return query.all()


if __name__ == "__main__":
    print("generateReport called with __main__")
    params = report_params(end_date=datetime.datetime.now(),start_date=(datetime.datetime.now() - datetime.timedelta(days=7)))
    params.query_data = filter_events(end_date=params.end_date,start_date=params.start_date)
    params.parse_query()
    create_spreadsheet()
