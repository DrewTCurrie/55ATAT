 #Created by Drew Currie on 09/19/2024
 #Last modified 09/19/2024 -Drew Currie

 #09/19/2024 Update: 
 #Automatic Report generation script. This script will be used to create a report every week on Friday at 5:00PM and the last day of every month at 5:00PM
 # In addition to generating the report at the end of the month, the script will move all data from the currentAttendanceEvents database table to 
 # the ArchiveAttendanceEvents database table, and then when verified the data has been transferred, it will empty the currentAttendanceEvents 
 # database table to prepare for the next month of attendance events.

#10/17/2024 Update:
#Adding mailing feature to automatically send reports via an email client

#Libraries used:
from datetime import datetime, timedelta, date
import calendar
import sys, time
from reports import generateReport
#Add to system path the directory of the API Functions to access the utilities functions
from APIFuncs import utils

#Import mailing service
from reports import mailer

def weekly_reports(app, mail):
    print("Weekly report generation called.")
    fileName = generateReport.generate_spreadsheet(start_date=(datetime.now() - timedelta(weeks= 1)).strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
    print(fileName)
    mailer.SendWeeklyReport(app, mail, fileName)
    #TODO: Link with flaskMail to send an email with the attachment.




def monthly_reports(app, mail):
    print("Montly report generation called.")
    today = datetime.now()
    First_Day_Of_The_Month = today.replace(day = 1, hour = 0, minute = 0, second = 0, microsecond = 0)
    fileName = generateReport.generate_spreadsheet(start_date=(First_Day_Of_The_Month.strftime("%Y-%m-%dT%H:%M:%S.%fZ")))
    mailer.SendMonthlyReport(app, mail, fileName)
    print(fileName)
    
if __name__ == '__main__':
        sys.exit(print("Do not run this file directly!"))
 