 #Created by Drew Currie on 09/19/2024
 #Last modified 09/19/2024 -Drew Currie

 #09/19/2024 Update: 
 #Automatic Report generation script. This script will be used to create a report every week on Friday at 5:00PM and the last day of every month at 5:00PM
 # In addition to generating the report at the end of the month, the script will move all data from the currentAttendanceEvents database table to 
 # the ArchiveAttendanceEvents database table, and then when verified the data has been transferred, it will empty the currentAttendanceEvents 
 # database table to prepare for the next month of attendance events.


#Libraries used:
from datetime import datetime, timedelta
import sys
from reports import generateReport
#Add to system path the directory of the API Functions to access the utilities functions
sys.path.insert(0, '/home/drew/Documents/capstone/55ATAT/APIFuncs')
import utils





def weekly_reports():
    print("Weekly report generation called.")
    fileName = generateReport.generate_spreadsheet(start_date=(datetime.now() - timedelta(weeks= 1)).strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
    print(fileName)
    #TODO: Link with flaskMail to send an email with the attachment. 



def monthly_reports():
    print("Montly report generation called.")
if __name__ == '__main__':
        sys.exit(weekly_reports())
        fileName = generateReport.generate_spreadsheet(start_date=(datetime.now() - timedelta(weeks= 1)).strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        print(fileName)