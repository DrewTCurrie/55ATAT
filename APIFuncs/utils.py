#Utilities for accessing the database
# Drew Currie
# Last Updated 09/19/2024

#This file provides a series of useful functions for accessing the MariaDB database
#Each of the functions is documented in the declaration of the function



import collections
import json

import sqlalchemy.cyextension
import MariaDBapi as api
import JSONHandler as jsonhandler
import sqlalchemy
from sqlalchemy import delete, select, inspect
import uuid
from datetime import datetime
import random
from sqlalchemy.ext.declarative import declarative_base
import sys
import os

def GetUserInitials(UserID, Session):
    # Check the "Attendee" table for the UserID passed in (ID) and then get the Attendee's initials

    AttendeeInitials = Session.query(api.Attendee).get(UserID)
    #Check if the ID corresponds to an Attendee

    # If not found, Session.query returns "None"
    # If not found return error code 400
    # If found, the intials. Writting to terminal output as debugging tool.

    if(AttendeeInitials == None):
        #print("Error. Unknown UserID")
        return(400)
    else:
        #print("User Initials Found: " + AttendeeInitials.AttendeeInitials)
        return(AttendeeInitials.AttendeeInitials)


#This function pulls all of the user initals from the database.
def getAllUserInitials():
    #Create Sql Alchemy Session
    Session = sqlalchemy.orm.sessionmaker()
    Session.configure(bind=api.engine)
    Session = Session()
    #Initialize Query for all Attendee Initials
    query = Session.query(api.Attendee.AttendeeInitials).all()
    #Creating results by parsing the first (only value) in the row from the query
    results = json.dumps([r[0] for r in query])
    return results

def getRoles():
    # Create Sql Alchemy Session
    Session = sqlalchemy.orm.sessionmaker()
    Session.configure(bind=api.engine)
    Session = Session()
    #Get Column headers that are type boolean (Roles are uniquely this)
    #Get all columns
    columns = inspect(api.Attendee).columns
    #Pasrse columns for columns with type boolean.
    role_columns = [col.name for col in columns if isinstance(col.type, sqlalchemy.Boolean)]

    return role_columns

def NewAttendanceEvent(UserID):
    # Take User ID and create an attendance event in the "CurrentAttendanceEvents" table 
    # This function is generally going to be called by the Attendee Interface Sub-System 
    # to create a new attendance event when a QR code has been scanned.
    # 
    # Checks the database for valid user initials with the "GetUserInitials" function.


    #Take user ID from QR code as function input
    #Generate UUID for the EventID
    EventID = uuid.uuid4()

    #Query Database to get the Attendee Initials for the corresponding UserID
    # Open new session to the database.
    # NAESession = New Attendance Event Session 
    # Session is the syntax in sqlalchemy to connect to the DB
    api.Base.metadata.create_all(api.engine)

    NAESession = sqlalchemy.orm.sessionmaker()
    NAESession.configure(bind=api.engine)
    NAESession = NAESession()

    # Call get Initials function to find the user intials based on the UserID passed in
    UserInitials = GetUserInitials(UserID, NAESession)

    # Create an Object of type Attendance Event with all the parameters. Timestamp is automatically populated
    NewAttendanceEvent = api.AttendanceEvent(EventUUID=str(EventID), ID=UserID, AttendeeInitials=UserInitials, Timestamp = datetime.now(), Absent = False, TIL_Violation = 0, AdminInitials = "N/A", Comment = "N/A")
    # Try to add the attendance event to the database, if it fails, return error code 400, close session
    # If it suceeds, close the session and return 200 for success. 
    NAESession.add(NewAttendanceEvent)
    NAESession.commit()

    #try:
     #   NAESession.add(NewAttendanceEvent)
      #  NAESession.commit()
    #except:
    #    return(400)
    #finally:
    #    NAESession.close()
    #return(200)
def NewAttendee(JSONFilePath):
    Error = 0
    ValidID = 0
    ValidIDFailCount = 0
    while(ValidID != 400):
        #generate new userID and check if it already exists in the database. This should be basically a random string 
        RandomID = random.SystemRandom()
        newUserID = "PTCBZN-" + str(RandomID.randint(10000000000, 99999999999))
        #Start Database connection
        #NASession = New Attendee Session
        api.Base.metadata.create_all(api.engine)
        NASession = sqlalchemy.orm.sessionmaker()
        NASession.configure(bind=api.engine)
        NASession = NASession()
        #Query Database for a match to the ID
        ValidID = GetUserInitials(newUserID, NASession)
        if(ValidID == 400):
            #print("Found Valid ID")
            #print("Now Reading JSON")
            AttendeeJSON = jsonhandler.ReadJSON(JSONFilePath)
            #AttendeeInfo = jsonhandler.ParseJSON(AttendeeJSON)
            #print("Now Parsing JSON")
            #AttendeeJSON['AttendeeDetails'][0]['Client']
            #print("Now Creating Attendee Object")
            NewAttendee = api.Attendee(
                                       ID = newUserID,
                                       Client = AttendeeJSON['Client'],
                                       Employee = AttendeeJSON['Employee'],
                                       ABA_Earlychildhood = AttendeeJSON['ABA_Earlychildhood'],
                                       ABA_Teen = AttendeeJSON['ABA_Teen'],
                                       Occupational_Therapy = AttendeeJSON['Occupational_Therapy'],
                                       Speech_Therapy = AttendeeJSON['Speech_Therapy'],
                                       Administrator = AttendeeJSON['Administrator'],
                                       Employee_SPOT = AttendeeJSON['Employee_SPOT'],
                                       Employee_BCBA = AttendeeJSON['Employee_BCBA'],
                                       Employee_RBT = AttendeeJSON['Employee_RBT'],
                                       Employee_Other = AttendeeJSON['Employee_Other'],
                                       AttendeeInitials = AttendeeJSON['AttendeeInitials']
                                       )

            #print("Now Sending Attendee Object to Database")
            try:
                NASession.add(NewAttendee)
            except:
                print("Unable to write to database. Error 400")
                Error = 400
            else:
                NASession.commit()
                #print("Successfully added attendee to database.")
                Error = 200
            finally:
                NASession.close()
        else:
            ValidIDFailCount += ValidIDFailCount
        if(ValidIDFailCount > 3):
            #If unable to create a valid ID in three tries, error out and return error code 1
            return(1)
        #Error code 400 means data not found, this is a success in this case because it means there is no matching ID
        else:
            return(Error)

#This function creates a NewAttendee when prompted from the webpage.
def NewAttendeeFromWeb(AttendeeJSON):
    Error = 0
    ValidID = 0
    ValidIDFailCount = 0
    while (ValidID != 400):
        # generate new userID and check if it already exists in the database. This should be basically a random string
        RandomID = random.SystemRandom()
        newUserID = "PTCBZN-" + str(RandomID.randint(10000000000, 99999999999))
        # Start Database connection
        # NASession = New Attendee Session
        api.Base.metadata.create_all(api.engine)
        NASession = sqlalchemy.orm.sessionmaker()
        NASession.configure(bind=api.engine)
        NASession = NASession()
        # Query Database for a match to the ID
        ValidID = GetUserInitials(newUserID, NASession)
        if (ValidID == 400):
            NewAttendee = api.Attendee(
                ID=newUserID,
                Client=AttendeeJSON['Client'],
                Employee=AttendeeJSON['Employee'],
                ABA_Earlychildhood=AttendeeJSON['ABA_Earlychildhood'],
                ABA_Teen=AttendeeJSON['ABA_Teen'],
                Occupational_Therapy=AttendeeJSON['Occupational_Therapy'],
                Speech_Therapy=AttendeeJSON['Speech_Therapy'],
                Administrator=AttendeeJSON['Administrator'],
                Employee_SPOT=AttendeeJSON['Employee_SPOT'],
                Employee_BCBA=AttendeeJSON['Employee_BCBA'],
                Employee_RBT=AttendeeJSON['Employee_RBT'],
                Employee_Other=AttendeeJSON['Employee_Other'],
                AttendeeInitials=AttendeeJSON['AttendeeInitials']
            )

            # print("Now Sending Attendee Object to Database")
            NASession.add(NewAttendee)
            NASession.commit()
            NASession.close()
            return newUserID
        else:
            ValidIDFailCount += ValidIDFailCount
        if (ValidIDFailCount > 3):
            # If unable to create a valid ID in three tries, error out and return error code 1
            return (1)
        # Error code 400 means data not found, this is a success in this case because it means there is no matching ID
        else:
            return (Error)

def createAdministrator(AdministratorJSON):
    #Create SqlAlchemy Session
    api.Base.metadata.create_all(api.engine)
    NASession = sqlalchemy.orm.sessionmaker()
    NASession.configure(bind=api.engine)
    NASession = NASession()
    #Create NewAdministrator entry from AdministratorJSON
    NewAdministrator = api.Administrator(
        ID = AdministratorJSON['ID'],
        UserName = AdministratorJSON['username'],
        Password = AdministratorJSON['password']            #TODO: Create a function that encrypts + salts this, outside of utils.py
    )
    #Add to DB
    NASession.add(NewAdministrator)
    NASession.commit()
    NASession.close()

def GetAttendanceEvents(Initials):
    #Get all the attendance events within a specified date & time range
    SelectedRecords = select(api.AttendanceEvent).where(api.AttendanceEvent.AttendeeInitials == Initials)
    with api.engine.connect() as RTSession:
        for Record in RTSession.execute(SelectedRecords):
            print(Record)


def GetAttendanceReport(StartTimestamp, FILEPATH):
    SelectedRecords = select(api.AttendanceEvent).where(api.AttendanceEvent.Timestamp > StartTimestamp)

    with api.engine.connect() as RTSession:
        for Record in RTSession.execute(SelectedRecords):
            #print(Record)
            jsonhandler.PopulateJSONReport(FILEPATH, Record)

#Returns an Attendee given an AttendeeID
def getAttendee(AttendeeID):
    api.Base.metadata.create_all(api.engine)
    Session = sqlalchemy.orm.sessionmaker()
    Session.configure(bind=api.engine)
    Session = Session()
    query = Session.query(api.Attendee).filter_by(ID=AttendeeID).first()
    return query

def getAttendeeRole(AttendeeID):
    #Create Sqlalchemy Session
    api.Base.metadata.create_all(api.engine)
    Session = sqlalchemy.orm.sessionmaker()
    Session.configure(bind=api.engine)
    Session = Session()
    # Query Database for Attendee
    query = Session.query(api.Attendee).filter_by(ID=AttendeeID).first()
    #Get A list of all roles in database
    roles = getRoles()
    #Compare query columns to roles list.
    if query is not None:
        userRoles = [col for col in roles if getattr(query, col) == 1]
    return userRoles


def ClearAttendeeRecords():
        #CTSession = Clear Table Session
        api.Base.metadata.create_all(api.engine)
        CTSession = sqlalchemy.orm.sessionmaker()
        CTSession.configure(bind=api.engine)
        CTSession = CTSession()
        for ID in CTSession.query(api.Attendee.ID).distinct():
            Record = CTSession.query(api.Attendee).get(ID)
            CTSession.delete(Record)
        CTSession.commit()
        CTSession.close()

def ArchiveAttedanceRecords():
    api.Base.metadata.create_all(api.engine)
    #MTSession = Migrate Table Session
    CTSession = sqlalchemy.orm.sessionmaker()
    CTSession.configure(bind=api.engine)
    CTSession = CTSession()
    for ID in CTSession.query(api.AttendanceEvent.EventUUID).distinct():
        Record = CTSession.query(api.AttendanceEvent).get(ID)
        ArchivalRecord = api.ArchivalEvent(EventUUID = Record.EventUUID,ID=Record.ID, AttendeeInitials=Record.AttendeeInitials, Timestamp=Record.Timestamp, Absent=Record.Absent, TIL_Violation=Record.TIL_Violation, AdminInitials=Record.AdminInitials, Comment=Record.Comment)    
        CTSession.add(ArchivalRecord)
    CTSession.commit()
    CTSession.close()

def ClearArchivalAttendanceRecords():
    #CTSession = Clear Table Session
    api.Base.metadata.create_all(api.engine)
    CTSession = sqlalchemy.orm.sessionmaker()
    CTSession.configure(bind=api.engine)
    CTSession = CTSession()
    for ID in CTSession.query(api.ArchivalEvent.EventUUID).distinct():
        Record = CTSession.query(api.ArchivalEvent).get(ID)
        CTSession.delete(Record)
    CTSession.commit()
    CTSession.close()

def ClearAttendanceRecords():
        #CTSession = Clear Table Session
        api.Base.metadata.create_all(api.engine)
        CTSession = sqlalchemy.orm.sessionmaker()
        CTSession.configure(bind=api.engine)
        CTSession = CTSession()
        for ID in CTSession.query(api.AttendanceEvent.EventUUID).distinct():
            Record = CTSession.query(api.AttendanceEvent).get(ID)
            CTSession.delete(Record)
        CTSession.commit()
        CTSession.close()

def ClearAdministrators():
    #Create Sql Alchemy Session
    api.Base.metadata.create_all(api.engine)
    CTSession = sqlalchemy.orm.sessionmaker()
    CTSession.configure(bind=api.engine)
    CTSession = CTSession()
    #Query Database for all Administrators, Delete 1 by 1
    for ID in CTSession.query(api.Administrator.ID).distinct():
        Record = CTSession.query(api.Administrator).get(ID)
        CTSession.delete(Record)
    #Commit Changes and close session
    CTSession.commit()
    CTSession.close()

if __name__ == '__main__':
    sys.exit(GetAttendanceEvents())
