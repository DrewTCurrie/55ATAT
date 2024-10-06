 #Created by Drew Currie on 09/19/2024
 #Last modified 09/19/2024 -Drew Currie

 #09/19/2024 Update: 
 #Automatic Report generation script. This script will be used to create a report every week on Friday at 5:00PM and the last day of every month at 5:00PM
 # In addition to generating the report at the end of the month, the script will move all data from the currentAttendanceEvents database table to 
 # the ArchiveAttendanceEvents database table, and then when verified the data has been transferred, it will empty the currentAttendanceEvents 
 # database table to prepare for the next month of attendance events.


#Libraries used:
from datetime import datetime, timedelta, date
import calendar
import sys, time
from reports import generateReport
#Add to system path the directory of the API Functions to access the utilities functions
sys.path.insert(0, '/home/drew/Documents/capstone/55ATAT/APIFuncs')
import utils



def CheckReportsSchedule():
    print("Checking if reports need generated today")
    today = datetime.today()
    #Check if today is friday
    #Maps the days of the week on Monday = 0 through Sunday = 6
    if date.today().weekday() == 4:
         #If it is Friday create the weekly report
         weekly_reports()
    time.sleep(60)
    
    #Check if today is the last day of the month -> Must happen after week as month clears database
    #Maps the days of the current month in the current year to an index, with 1 being the last day of the month
    #If today is equal to the last day of the month create a report
    if calendar.monthrange(today.year, today.month)[1] == today.day:
         #If it is the last day of the month, generate monthly attendance report
         monthly_reports()
         #Delete archival records then move current records into archive
         #Archive records and then delete records from current attedance event table
         #This resets the database in prepartion for the new month
         utils.ClearArchivalAttendanceRecords()
         utils.ArchiveAttedanceRecords()
         utils.ClearAttendanceRecords()
    #If it is not the end of the month or friday do not create a report





def weekly_reports():
    print("Weekly report generation called.")
    fileName = generateReport.generate_spreadsheet(start_date=(datetime.now() - timedelta(weeks= 1)).strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
    print(fileName)
    #TODO: Link with flaskMail to send an email with the attachment. 



def monthly_reports():
    print("Montly report generation called.")
    fileName = generateReport.generate_spreadsheet(start_date=(datetime.now() - timedelta(weeks= 4)).strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
    print(fileName)
    
if __name__ == '__main__':
        sys.exit(CheckReportsSchedule())
 