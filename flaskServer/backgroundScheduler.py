#Created 10/19/2024 Drew Currie
#Last editted: 10/19/2024 DC
#Background task scheduler for the flask server
# These tasks include:
# 1: Creating reports on a weekly basis
# 2: Creating reports on a monthly basis
# 3: Removing files generated every week (old reports, profile pictures, and badges)

#This background process will run once a day at 9:00PM local time to the system


from datetime import datetime, timedelta, date
import calendar
import sys, time
#Add to system path the directory of the API Functions to access the utilities functions
from APIFuncs import utils
from reports import reportScheduler

#Import mailing service
from reports import mailer

#Import garbage collector 
import garbagecollector

def CheckEndOfWeek():
    print("Checking if today is the last day of the week.")
    today = datetime.today()
    if date.today().weekday() == 4:
        print("Today is the last day of the week.")
        return(True)
    else:
        print("Today is not the last day of the week.")
        return(False)
     
def CheckEndOfMonth():
    today = datetime.today()
    print("Checking if today is the last day of the month.")
    if calendar.monthrange(today.year, today.month)[1] == today.day:
        print("Today is the last day of the month.")
        return(True)
    else:
        print("Today is not the last day of the month.")
        return(False)


def MonthlyTasks(app, mail):
    #If it is the last day of the month, generate monthly attendance report
    reportScheduler.monthly_reports(app, mail)
    time.sleep(60)
    #Delete archival records then move current records into archive
    #Archive records and then delete records from current attedance event table
    #This resets the database in prepartion for the new month
    print("Clearing archival attendance records")
    utils.ClearArchivalAttendanceRecords()
    print("archiving current month's records")
    utils.ArchiveAttedanceRecords()
    print("Clearning current month's records")
    utils.ClearAttendanceRecords()
    #Run garbage collector on everything
    print("Running garbage collector")
    garbagecollector.CollectGarbage()


def WeeklyTasks(app, mail):
    reportScheduler.weekly_reports(app, mail)
    #Run the garbage collector
    time.sleep(60)
    garbagecollector.CollectGarbage()




def TaskScheduler(app, mail):
    print("Checking if background tasks need completed today:")
    if(CheckEndOfWeek()): 
        print("\tIt is the end of the week. Time to run weekly tasks!")
        WeeklyTasks(app, mail)
    if(CheckEndOfMonth()):
        print("\tIt is the end of the month. Time to run monthly tasks!")
        MonthlyTasks(app, mail)

if __name__ == '__main__':
    sys.exit(TaskScheduler())