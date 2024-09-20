 #Created by Drew Currie on 09/19/2024
 #Last modified 09/19/2024 -Drew Currie

 #09/19/2024 Update: 
 #Automatic Report generation script. This script will be used to create a report every week on Friday at 5:00PM and the last day of every month at 5:00PM
 # In addition to generating the report at the end of the month, the script will move all data from the currentAttendanceEvents database table to 
 # the ArchiveAttendanceEvents database table, and then when verified the data has been transferred, it will empty the currentAttendanceEvents 
 # database table to prepare for the next month of attendance events.


#Libraries used:
import datetime, sys

#Add to system path the directory of the API Functions to access the utilities functions
sys.path.insert(0, '/home/drew/Documents/capstone/55ATAT/APIFuncs')
import utils
import generateReport




def weekly_reports():
    start_date = datetime.today()
    end_date = start_day - timedelta(days=7)
    print("Time Frame to generate report for: " + start_date + " Through " + end_date)
    #fileName = generateReport.generate_spreadsheet(name, role, start_date, end_date)
    #Checking if file exists for a minute before throwing an error.
    #start_time = time.time()
    #dir = 'flaskServer/xlsx/'
    #print(dir+fileName)
    #while time.time() - start_time < 60:
    #    if os.path.isfile('/home/55ATAT/55ATAT/flaskServer/xlsx/'+fileName):
    #        print('found file')
    #    time.sleep(1)




#def monthly_reports():
#    start_date = data.get('startDate')
#    end_date = 
#    fileName = generateReport.generate_spreadsheet(name, role, start_date, end_date)
#    #Checking if file exists for a minute before throwing an error.
#    start_time = time.time()
#    dir = 'flaskServer/xlsx/'
#    print(dir+fileName)
#    while time.time() - start_time < 60:
#        if os.path.isfile('/home/55ATAT/55ATAT/flaskServer/xlsx/'+fileName):
#            print('found file')
#        time.sleep(1)


if __name__ == '__main__':
        sys.exit(weekly_reports())