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

def main():

    #Creating fake attendees and populating them to the database table "Attendees"
    numberOfAttendees = int(input("How many Attendees to create?:  "))
    Confirm = input("Confirm creating " + str(numberOfAttendees) + " number of new attendees? y/n:  ")
    if(Confirm == "n" or Confirm == "N"):
        return(1)
    print("Clearing old Attendees from database") 
    try:
        ClearAttendeeRecords = utils.ClearAttendeeRecords()
    except:
        print("Error: Unable to clear Attendee Records from Database")
        return(1)
    else:
        print("Sucessfully cleared Attendee Records")
    
    print("Clearing old AttendanceEvents from database")
    
    try:
        ClearAttendanceEventsRecords = utils.ClearAttendanceRecords()
    except:
        print("Unable to clear Attendance Event Records from the database")
        return(1)
    else:
        print("Sucessfully cleared Attendance Event Records from the database")

    try:
        CA.CreateFakeAttendees(numberOfAttendees, Confirm)
    except:
        print("Error in Creating Attendees")
    #else:
        #print(str(numberOfAttendees) + " Attendees Sucessfully Created.")
    
    for AttendeeNumber in range(numberOfAttendees):
        try:
            utils.NewAttendee(os.path.join(sys.path[0], "AttendeeJSONFiles/TestJSON"+str(AttendeeNumber+1)+".json"))
        except:
            print("Unable to write attendee " + str(AttendeeNumber+1) + " to database.")
        #else:
            #print("Successfully wrote Attendee: " +str(AttendeeNumber+1) + str(" to Attendee table"))

#Creating fake Attendance Events and populating the events to the "CurrentAttendanceEvents" table

    numberOfEvents = int(input("How many AttendanceEvents to create?:  "))
    Confirm = input("Confirm creating " + str(numberOfEvents) + " number of new Attendance Events? y/n:  ")
    if(Confirm == "n" or Confirm == "N"):
        return(1)
    #Create new session for attandance events:
    api.Base.metadata.create_all(api.engine)
    AttendeeSession = sqlalchemy.orm.sessionmaker()
    AttendeeSession.configure(bind=api.engine)
    AttendeeSession = AttendeeSession()
    AttendeeList = []
    for AttendeeID in AttendeeSession.query(api.Attendee.ID).distinct():
        Record = AttendeeSession.query(api.Attendee).get(AttendeeID)
        AttendeeList.append(Record.ID)
 
    for events in range(numberOfEvents):

        #timeDelay = random.randint(1,3)
        print("Delaying for: " + str(timeDelay) + " seconds")
        #time.sleep(timeDelay)

        AttendeeID = AttendeeList[random.randint(0, (len(AttendeeList)-1))]
        Result = utils.NewAttendanceEvent(AttendeeID)
        if(Result == 400):
            print("Could not write to database.")
        else:
            print("successfully written to database")
         

    #Now Reading selected rec ords back from the database:

    OperatingMode = '1'
    while(OperatingMode != '0'):
        OperatingMode = str(input("Press 1 to search Attendance Events by Initials. Press 2 to search for Attendance Events by TimeStamp Range. Press 0 to quit: "))
        if OperatingMode == '1':
            AttendeeInitials = str(input("Enter attendee initials to search for: "))
            utils.GetAttendanceEvents(AttendeeInitials)
        elif OperatingMode == '2':
            StartYear = int(input("Enter Starting year: "))
            if StartYear < 2024:
                StartYear = int(input("Error Invalid starting year. Minimum year of 2024. Re-enter year: "))
            else:
                StartMonth = int(input("Enter month in numerical format, without a leading 0: "))
                if(StartMonth > 12 or StartMonth < 1):
                    StartMonth = int(input("Error invalid starting month. Enter a month between 1-12: "))
                else:
                    StartDay = int(input("Enter a starting day from 1-31 with no leading 0:  "))
                    if(StartDay < 1 or StartDay > 31):
                        StartHours = int(input("Enter starting hours from 0-24: "))
                    else:
                        StartHours = int(input("Enter starting hour between 0-24"))
                        if(StartHours > 24 or StartHours < 0):
                            StartHours = int(input("Error invalid hours. Enter hours between 0-24: "))
                        else:
                            StartMinutes = int(input("Enter starting minutes from 0-60: "))
                            if(StartMinutes > 60 or StartMinutes < 0):
                                StartMinutes = int(input("Error invalid start minutes: "))
                            else:
                                StartSeconds = int(input("Enter start seconds from 0-60: "))
                                if(StartSeconds > 60 or StartSeconds < 0):
                                    StartSeconds = int(input("Error enter start seconds between 0-60: "))
                                else:
                                    #utils.GetAttendanceReport(datetime.datetime(StartYear, StartMonth, StartDay, StartHours, StartMinutes, StartSeconds).strftime)
                                    TimeStamp = datetime.datetime(StartYear, StartMonth, StartDay, StartHours, StartMinutes, StartSeconds).strftime('%YY-%m-%d %H:%M:%S')
                                    #print(TimeStamp)
                                    ReportJSON =  os.path.join(sys.path[0], "AttendanceReports/Reports/"+"AttendanceReport-20"+datetime.datetime.now().strftime('%y-%m-%d') + ".json")  
                                    
                                    FileExists = os.path.isfile(ReportJSON)
                                    if(FileExists == False):
                                        with open(ReportJSON, "w") as fp:
                                            pass
                                        fp.close()
                                    utils.GetAttendanceReport(TimeStamp, ReportJSON)
    return(0)
    

if __name__ == '__main__':
    sys.exit(main())
