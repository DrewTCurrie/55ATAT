import sys
import os
sys.path.append(os.path.join(sys.path[0], '../APIFuncs'))
import utils
import MariaDBapi as api
import CreateAttendees as CA
import time
import sqlalchemy
import random
import datetime

#Creating an array of the number of attendees to randomly create per test:
#Increase for 50 through 1000 attendees in the attendees table
    
#Increase for 200 attendnace events per day for 1-14 days
AttendanceEventCount = [200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 200, 3200, 6000]
TotalAttendanceEvents = [200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800, 6000, 12000]

def main():
    try:
        utils.ClearAttendeeRecords()
    except:
        print("Error: Unable to clear Attendee Records from Database")
        return(1)
    else:
        print("Suessfully cleared attendee Records")
                
    try:
        utils.ClearAttendanceRecords()
    except:
        print("Error: Unable to clear attendance Records from Database")
        return(1)
    else:
        print("Sucessfully cleared attendance records.")
    print("Creating 50 Fake attendees")
    CA.CreateFakeAttendees(50, "y")
    for AttendeeNumber in range(50):
        try:
            utils.NewAttendee(os.path.join(sys.path[0], "AttendeeJSONFiles/TestJSON"+str(AttendeeNumber+1)+".json"))
        except:
            print("Unable to write attendee " + str(AttendeeNumber+1) + " to database.")
            
    for numberofAttendanceEvents in AttendanceEventCount:
        print(numberofAttendanceEvents)

    #Create fake attendees for the test

        #Connect to MariaDB Database
        api.Base.metadata.create_all(api.engine)
        AttendeeSession = sqlalchemy.orm.sessionmaker()
        #Bind to database engine
        AttendeeSession.configure(bind=api.engine)
        #Establish AttendeeSession object
        AttendeeSession = AttendeeSession()
            
        #Get list of attendee IDs to randomly create attendance events
        AttendeeList = []
        for AttendeeID in AttendeeSession.query(api.Attendee.ID).distinct():
            Record = AttendeeSession.query(api.Attendee).get(AttendeeID)
            AttendeeList.append(Record.ID)

        #Populate attendance events
        for eventNumber in range(numberofAttendanceEvents):
            #Number of seconds to randomly delay to create unique time stamp data
            timeDelay = 1
            print("Writing Attendance Event: " 
                    + str(eventNumber+1) + " Of " + str(numberofAttendanceEvents) + 
                    " With: " + str(50) +
                    " Attendees in the Database")
            AttendeeID = AttendeeList[random.randint(0, (len(AttendeeList)-1))]
            Result = utils.NewAttendanceEvent(AttendeeID)
            if(Result == 400):
                print("Could not write " + str(eventNumber) + " to database.")
            else:
                print("Sucesfully wrote attendance event: "
                           + str(eventNumber+1) + " of " + str(numberofAttendanceEvents))
                print("Delaying for: " + str(timeDelay) + " Seconds")
                time.sleep(timeDelay)

            #Read back attendance events and record time to complete
            TimeStamp = datetime.datetime(2024, 4, 20, 0, 0, 0).strftime('%YY-%m-%d %H:%M:%S')
            ReportJSON =  os.path.join(sys.path[0], "AttendanceReports/Reports/"+"AttendanceReport"
                                       +str(numberofAttendanceEvents)+ "Events with " + 
                                       str(50)+"20"+datetime.datetime.now()
                                       .strftime('%y-%m-%d') + ".json")
            with open(ReportJSON, "w") as fp:
                pass
            fp.close()
            StartTime = time.time()
            utils.GetAttendanceReport(TimeStamp, ReportJSON)
            EndTime = time.time()
            ExecutionTime = EndTime - StartTime
            print("Execution time for " + str(numberofAttendanceEvents) + " Events with "
                   + str(50) + "Attendees in the database: " + str(ExecutionTime))
            #Write results data to the results text file for data collection
            ResultsFile = open("/home/drew/55ATAT/TestBenches/testresult.txt", "a")
            ResultsFile.write("\nExecution time for " + str(numberofAttendanceEvents) + " Events with 50 Attendees in the database: " + str(ExecutionTime) + " [Seconds]")
            ResultsFile.close()
               
    return(0)
    

if __name__ == '__main__':
    sys.exit(main())




