# generateReport
# Sam Lovering
# Last Updated 9/19/2024 - Drew Currie
#
# When query params are passed in this program will parse them, query the systems' database
# then create an Excel spreadsheet based on the results.
#
# Big Ticket TODOs:
# 1. Create Aggregate information like in original
# 2. Make iteration not delete from behind
# 3. implement types.
# 4. IMPLEMENT ROLES


#09/19/2024 Update: Updated system path to use absolute pathing instead of relative pathing. 
# For some reason the relative pathing breaks the system links on the RaspberryPi but only on
# the raspberryPi. 

import datetime
import os
import collections
import sqlalchemy
import xlsxwriter
import json
import sys
from sqlalchemy import and_
from sqlalchemy.orm import declarative_base

#Using absolute pathing seems to work but relative pathing break. Not really sure why.
#We'll have to figureo out why this is
#TO-DO: Figure out why relative pathing breaks python includes only on the RaspberryPi
sys.path.append(os.path.join(sys.path[0], '/home/55ATAT/55ATAT'))
sys.path.append(os.path.join(sys.path[0], '/home/55ATAT/55ATAT/APIFuncs'))

from APIFuncs import MariaDBapi as api
from APIFuncs import utils

class report_params:
    def __init__(self, name=None, start_date=None, end_date=None):
        self.name = name
        #None checking for dates.
        if start_date is None:
            self.start_date = (datetime.datetime.now() - datetime.timedelta(days=7))
        else:
            self.start_date = datetime.datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        if end_date is None:
            self.end_date = datetime.datetime.now()
        else:
            self.end_date = datetime.datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        self.roles = collections.defaultdict(list)
        self.query_data = ((),)
        self.attendance_data = collections.defaultdict(list)

    # Generates a range of dates using the report params.
    def generate_date_range(self):
        date_list = []
        current_date = self.start_date
        while current_date <= self.end_date:
            date_list.append(current_date)
            current_date += datetime.timedelta(days=1)
        date_list = [date for date in date_list if date.weekday() < 5]
        return date_list

    #This parses the query, and creates a bunch of attendance data class objects.
    def parse_query(self):
        #Get Roles
        roles = utils.getRoles()
        print(roles)
        #Initialize DB Session
        Session = sqlalchemy.orm.sessionmaker()
        Session.configure(bind=api.engine)
        Session = Session()
        for event in self.query_data:
            #Add Event data to attendance data
            self.attendance_data[event.AttendeeInitials].append(event)
            #Query for Roles by ID
            user_row = Session.query(api.Attendee).filter(
                api.Attendee.AttendeeInitials == event.AttendeeInitials).one_or_none()
            #Checks to see if boolean columns in user_row are true, appends to user roles.
            if user_row is not None:
                userRoles = [col for col in roles if getattr(user_row, col) == 1]
                self.roles[event.AttendeeInitials] = userRoles


def create_spreadsheet(params):
    #Initialize Spreadsheet
    #Create Excel file with meta data
    fileName = ('attendanceReport'+datetime.datetime.now().strftime("%m%d%H%M")+'.xlsx')
    workbook = xlsxwriter.Workbook('/home/55ATAT/55ATAT/flaskServer/xlsx/'+fileName)
    worksheet = workbook.add_worksheet()

    #WORKBOOK FORMATS
    # Header format
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
    #Formatting for Individual Dates
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

    # Merge and format the main title
    worksheet.merge_range('C1:S1', 'Peach Tree Client Attendance Tracker', header_format)
    # Absence Type Key section
    worksheet.write('A2', 'Absence Type Key:', workbook.add_format({'bold': True}))
    worksheet.write('A3', 'Warning: Do not insert rows!', workbook.add_format({'font_color': 'red', 'bold': True}))

    # Merge and write the month dynamically based on the start date
    worksheet.merge_range('A4:B4', 'Month: {}'.format(params.start_date.strftime('%B %Y')), header_format)

    # Define the absence types and formats
    keys = ['P', 'C', 'T', 'A', 'I', 'L', '#', 'H', 'X']
    key_descriptions = ['Present', 'Approved Cancellation', 'Tardy (by Unit)', 'Unapp. Cancel. (by day)',
                        'Incomp. Session (by Unit)', 'Late Pickup (by Unit)', 'Reduced by PTC (by hour)', 'PTC Holiday',
                        'Not Scheduled']
    colors = ['#fdebd7', '#6db260', '#f6ab58', '#c00000', '#f6ab58', '#f6ab58', '#ffd966', '#99bcc9', '#d9d9d9']

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
        worksheet.write(1, (i * 2) + 2, key, format_key)
        worksheet.write(2, (i * 2) + 2, desc, format_desc)

    # Note section
    worksheet.merge_range('X2:AA3',
                          'Note: \nIf a client’s attendance is close to lower limit, and they have been called off many times, their actual attendance ratio should be calculated manually',
                          note_format)

    #Get Date List from Class
    date_list = params.generate_date_range()

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
    worksheet.set_column(2, len(date_list) if len(dates) > 18 else 18, 5)

    #Populate with Database Data.
    for index, events in enumerate(params.attendance_data.items()):
        #Write Client Information
        #Assign roles based on if they are appended to the events
        roles = params.roles[events[0]]
        print(roles)
        roleString = ''
        if roles:
            if roles[0] == 'Employee':
                roleString = roleString + 'E/'
                if 'Employee_BCBA' in roles:
                    roleString = roleString + 'BCBA'
                if 'Employee_SPOT' in roles:
                    roleString = roleString + 'SPOT'
                if 'Administrator' in roles:
                    roleString = roleString + 'Admin'
            elif roles[0] == 'Client':
                roleString = roleString + 'C/'
                if len(roles) > 2:
                    roleString = roleString + 'Multiple'
                else:
                    if 'ABA_Teen' in roles:
                        roleString = roleString + 'ABA Teen'
                    if 'ABA_Earlychildhood' in roles:
                        roleString = roleString + 'ABA Early'
                    if 'Speech_Therapy' in roles:
                        roleString = roleString + 'Speech'
                    if 'Occupational_Therapy' in roles:
                        roleString = roleString + 'OT'
        worksheet.write(index + 5, 0, roleString)

        #Write Attendee Initials
        worksheet.write(index + 5, 1, events[0])

        #Write Attendance Data
        for event in events[1]:
            #Convert DB Timestamp into Datetime Object
            event_date = event.Timestamp
            #Iterate and add to worksheet.
            for colIndex, date in enumerate(date_list):
                if event_date.date() == date.date():
                    if event.Absent == True:
                        worksheet.write(index + 5, colIndex + 2, "A", unapproved_cancel_format)
                        worksheet.write_comment(index + 5, colIndex + 2, f"{event.AdminInitials}\n{event.Timestamp}",
                                                {'author': event.AdminInitials})
                    elif event.TIL_Violation == True:
                        worksheet.write(index + 5, colIndex + 2, "T", tardy_format)
                        worksheet.write_comment(index + 5, colIndex + 2, f"{event.AdminInitials}\n{event.Timestamp}",
                                                {'author': event.AdminInitials})
                    else:
                        worksheet.write(index + 5, colIndex + 2, "P", present_format)

    # Close the workbook
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


# This function creates a database query based on optional params passed by reportModal web component.
def filter_events(name=None, role=None, start_date=None, end_date=None):
    #Create Session
    Session = sqlalchemy.orm.sessionmaker()
    Session.configure(bind=api.engine)
    Session = Session()

    #Initalize Query
    query = Session.query(api.AttendanceEvent)

    #Create Filters
    filters = []
    if name is not None:
        #Search database for attendance events with same AttendeeInitials
        filters.append(api.AttendanceEvent.AttendeeInitials == name)
    if role is not None:
        if hasattr(api.Attendee, role):
            roleFilter = (getattr(api.Attendee, role) == 1)
            query = query.join(api.Attendee, api.AttendanceEvent.ID == api.Attendee.ID).filter(roleFilter)
    if start_date is not None:
        #Search database for attendance events that are after start_date
        filters.append(api.AttendanceEvent.Timestamp >= start_date)
    else:
        #if no start_date, create one for one week ago
        filters.append(api.AttendanceEvent.Timestamp >= (datetime.datetime.now() - datetime.timedelta(days=7)))
    if end_date is not None:
        # Search database for attendance events that are before end date
        filters.append(api.AttendanceEvent.Timestamp <= end_date)
    else:
        #if no end_date create one for now.
        filters.append(api.AttendanceEvent.Timestamp <= datetime.datetime.now())

    #Write filters to query
    query = query.filter(and_(*filters))
    return query.all()


#This function does generates a report when it is called outside of the main function
def generate_spreadsheet(name=None, role=None, start_date=None, end_date=None):
    print("generateReport called with generate_spreadsheet()")
    params = report_params(name, start_date, end_date)
    params.query_data = filter_events(name=name, role=role, start_date=start_date, end_date=end_date)
    params.parse_query()
    fileName = create_spreadsheet(params)
    return fileName


if __name__ == "__main__":
    print("generateReport called with __main__")
    generate_spreadsheet()
