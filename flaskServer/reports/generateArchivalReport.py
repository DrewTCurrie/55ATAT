# generateArchivalReport
# Sam Lovering
# Last Updated 12/7/2024
#
# This functions very similarly to generateReport, however there are no custom parameters, and calls from
# archivalEvents. When query params are passed in this program will parse them, query the systems' database then
# create an Excel spreadsheet based on the results.
import collections
import datetime

import sqlalchemy
import xlsxwriter

from APIFuncs import MariaDBapi as api
from APIFuncs import utils

class report_params:
    def __init__(self, name=None, eventTypes=None, start_date=None, end_date=None):
        self.name = name
        self.eventTypes = eventTypes
        #None checking for dates.
        if start_date is None or start_date == "Invalid Date":
            self.start_date = (datetime.datetime.now() - datetime.timedelta(days=7))
        else:
            self.start_date = datetime.datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        if end_date is None or end_date == "Invalid Date":
            self.end_date = datetime.datetime.now()
        else:
            self.end_date = datetime.datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        self.roles = collections.defaultdict(list)
        self.query_data = ((),)
        self.attendance_data = collections.defaultdict(list)

    # This function gets all the events in Archival Events, and sets start_date and end_date to the first and last timestamp.
    def get_events(self):
        # Create Session
        Session = sqlalchemy.orm.sessionmaker()
        Session.configure(bind=api.engine)
        Session = Session()

        # Initalize Query and get entire contents
        query = Session.query(api.ArchivalEvent).all()

        #Assign start_date and end_date
        if query:
            timestamps = [row.Timestamp for row in query]
            self.start_date = min(timestamps)
            self.end_date = max(timestamps)
        #assign query to query_data
        self.query_data = query
        Session.close()




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
        #Initialize DB Session
        Session = sqlalchemy.orm.sessionmaker()
        Session.configure(bind=api.engine)
        Session = Session()
        for event in self.query_data:
            #Add Event data to attendance data
            self.attendance_data[event.AttendeeInitials].append(event)
            #Query for Roles by ID
            user_row = Session.query(api.Attendee).filter(
                api.Attendee.ID == event.ID).one_or_none()
            #Checks to see if boolean columns in user_row are true, appends to user roles.
            if user_row is not None:
                userRoles = [col for col in roles if getattr(user_row, col) == 1]
                self.roles[event.AttendeeInitials] = userRoles

#Create a shreadsheet
def create_spreadsheet(params):
    #Initialize Spreadsheet
    #Create Excel file with meta data
    fileName = ('archiveattendanceReport'+datetime.datetime.now().strftime("%m%d%H%M")+'.xlsx')
    workbook = xlsxwriter.Workbook('flaskServer/xlsx/'+fileName)
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
    date_format = workbook.add_format({
        'bold': True,
        'font_color': 'black',
        'align': 'left',
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
    not_scheduled = workbook.add_format({
        'bg_color': '#d9d9d9',
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

    #Get Date List from Class
    date_list = params.generate_date_range()

    # Write days of the week (e.g., Thur, Fri, etc.)
    days_of_week = [date.strftime('%a') for date in date_list]
    worksheet.write_row('C4', days_of_week, header_format)

    # Write the dates (e.g., 1, 2, 3, etc.)
    dates = [date.strftime('%d') for date in date_list]
    worksheet.write_row('C5', dates, date_format)

    #Add Column Headers for "type" and "client"
    worksheet.write('A5', "Type", header_format)
    worksheet.write('B5', "Attendee", header_format)

    # Adjust column widths
    worksheet.set_column('A:A', 10)
    worksheet.set_column('B:B', 15)
    worksheet.set_column(2, len(date_list) if len(dates) > 18 else 18, 6)

    #Populate with Database Data.
    for index, events in enumerate(params.attendance_data.items()):
        #Write Client Information
        #Assign roles based on if they are appended to the events
        roles = params.roles[events[0]]
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
        filled_columns = {}
        #Write Attendance Data
        for event in events[1]:
            #Convert DB Timestamp into Datetime Object
            event_date = event.Timestamp
            #Track Written to Columns
            #Iterate and add to worksheet.
            for colIndex, date in enumerate(date_list):
                if event_date.date() == date.date():
                    filled_columns[colIndex] = True
                    if event.Absent == True:
                        worksheet.write(index + 5, colIndex + 2, "A", unapproved_cancel_format)
                        worksheet.write_comment(index + 5, colIndex + 2, f"{event.AdminInitials}\n{event.Comment}",
                                                {'author': event.AdminInitials})
                    elif event.TIL_Violation == True:
                        worksheet.write(index + 5, colIndex + 2, "T", tardy_format)
                        worksheet.write_comment(index + 5, colIndex + 2, f"{event.AdminInitials}\n{event.Comment}",
                                                {'author': event.AdminInitials})
                    else:
                        worksheet.write(index + 5, colIndex + 2, "P", present_format)

        #Fill remaining blank spots with 'X' for not scheduled.
        for colIndex, date in enumerate(date_list):
            if colIndex not in filled_columns:
                worksheet.write(index + 5, colIndex + 2, "X", not_scheduled)
    endrow = index +5
    endCol = colIndex+2
    #Set autofilter for names + roles column.
    worksheet.autofilter(4, 0, endrow, endCol)
    # Close the workbook
    workbook.close()
    return fileName

#This function does generates a report when it is called outside of the main function
def generate_spreadsheet():
    print("generateReport called with generate_spreadsheet()")
    params = report_params()
    params.get_events()
    params.parse_query()
    fileName = create_spreadsheet(params)
    return fileName

if __name__ == "__main__":
    print("generateReport called with __main__")
    generate_spreadsheet()