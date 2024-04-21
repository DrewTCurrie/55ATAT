import MariaDBapi as api
import JSONHandler as jsonhandler
import sqlalchemy
import uuid
from datetime import datetime
import random
from sqlalchemy.ext.declarative import declarative_base


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
    NewAttendanceEvent = api.AttendanceEvent(EventUUID=str(EventID), ID=str(UserID), AttendeeInitials=UserInitials)
    # Try to add the attendance event to the database, if it fails, return error code 400, close session
    # If it suceeds, close the session and return 200 for success. 
    try:
        NAESession.add(NewAttendanceEvent)
        NAESession.commit()
    except:
        return(400)
    finally:
        NAESession.close()
    return(200)



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
            print("Found Valid ID")
            print("Now Reading JSON")
            AttendeeJSON = jsonhandler.ReadJSON(JSONFilePath)
            #AttendeeInfo = jsonhandler.ParseJSON(AttendeeJSON)
            print("Now Parsing JSON")
            #AttendeeJSON['AttendeeDetails'][0]['Client']
            print("Now Creating Attendee Object")
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
            
            print("Now Sending Attendee Object to Database")
            try:
                NASession.add(NewAttendee)      
            except:
                print("Unable to write to database. Error 400")
                Error = 400
            else:
                NASession.commit()
                print("Successfully added attendee to database.")
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
