import sys
import os
sys.path.append(os.path.join(sys.path[0], '../APIFuncs'))
import utils
import MariaDBapi as api
import CreateAttendees as CA
import time
import sqlalchemy
import random

import tqdm

def main():

    #Creating fake attendees and populating them to the database table "Attendees"
    numberOfAttendees = int(input("How many Attendees to create?:  "))
    Confirm = input("Confirm creating " + str(numberOfAttendees) + " number of new attendees? y/n:  ")
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
    else:
        print(str(numberOfAttendees) + " Attendees Sucessfully Created.")
    
    for AttendeeNumber in range(numberOfAttendees):
        try:
            utils.NewAttendee(os.path.join(sys.path[0], "AttendeeJSONFiles/TestJSON"+str(AttendeeNumber)+".json"))
        except:
            print("Unable to write attendee " + str(AttendeeNumber+1) + " to database.")
        else:
            print("Successfully wrote Attendee: " +str(AttendeeNumber+1) + str(" to Attendee table"))

#Creating fake Attendance Events and populating the events to the "CurrentAttendanceEvents" table

    numberOfEvents = int(input("How many AttendanceEvents to create?:  "))
    Confirm = input("Confirm creating " + str(numberOfEvents) + " number of new Attendance Events? y/n:  ")

    #Create new session for attandance events:
    api.Base.metadata.create_all(api.engine)
    AttendeeSession = sqlalchemy.orm.sessionmaker()
    AttendeeSession.configure(bind=api.engine)
    AttendeeSession = AttendeeSession()
    AttendeeList = []
    for AttendeeID in tqdm(AttendeeSession.query(api.Attendee.ID).distinct()):
        Record = AttendeeSession.query(api.Attendee).get(AttendeeID)
        AttendeeList.append(Record.ID)
    #print(AttendeeList)
    print(len(AttendeeList))
    for events in tqdm(range(numberOfEvents)):
        AttendeeID = AttendeeList[random.randint(0, (len(AttendeeList)-1))]
        Result = utils.NewAttendanceEvent(AttendeeID)
        if(Result == 400):
            print("Could not write to database.")
        else:
            print("successfully written to database")
        timeDelay = random.randint(0,360)
        print("Delaying for: " + str(timeDelay) + " seconds")
        time.sleep(random.randint(0,360))
    
    return(0)
    

if __name__ == '__main__':
    sys.exit(main())