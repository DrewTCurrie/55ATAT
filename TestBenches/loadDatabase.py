import datetime
import json
import os
import random
import string
import sys

import pytz
import sqlalchemy
import uuid

sys.path.append(os.path.join(sys.path[0], '/home/55ATAT/55ATAT'))
sys.path.append(os.path.join(sys.path[0], '/home/55ATAT/55ATAT/APIFuncs'))

from APIFuncs import MariaDBapi as api
from APIFuncs import utils


# Todo, create a way to load attendance events associated with an attendee
def loadAttendees():
    directory = 'AttendeeJSONFiles/'
    file_paths = [os.path.join(directory,file) for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
    for file in file_paths:

        utils.NewAttendee(file)

def create_attendees_and_events():
    #Start out by cleaning the database
    utils.ClearAttendeeRecords()
    utils.ClearAttendanceRecords()

    #Open up DB Session
    Session = sqlalchemy.orm.sessionmaker()
    Session.configure(bind=api.engine)
    Session = Session()

    #Generate a bunch of Attendees
    for i in range(100):
        AttendeeJSON = create_attendees()
        RandomID = random.SystemRandom()
        newUserID = "PTCBZN-" + str(RandomID.randint(10000000000, 99999999999))
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
        Session.add(NewAttendee)
        #Make 10 attendance events for each attendee starting from today
        for i in range(10):
            date = datetime.datetime.now()
            mst = pytz.timezone('America/Denver')
            date = mst.localize(date)
            EventID = RandomID.randint(100000000, 999999999)
            NewAttendanceEvent = api.AttendanceEvent(EventUUID=uuid.uuid4(), ID=newUserID, AttendeeInitials=AttendeeJSON['AttendeeInitials'],
                                                     Timestamp=(date - datetime.timedelta(days=i)), Absent=False, TIL_Violation=0,
                                                     AdminInitials="N/A", Comment="N/A")
            Session.add(NewAttendanceEvent)
    Session.commit()
    Session.close()


def create_attendees():
    # Create python dictionary to hold all the randomly generated details for the imaginary attendee
    AttendeeDetails = {
        "Client": False,
        "Employee": False,
        "ABA_Earlychildhood": False,
        "ABA_Teen": False,
        "Occupational_Therapy": False,
        "Speech_Therapy": False,
        "Administrator": False,
        "Employee_SPOT": False,
        "Employee_BCBA": False,
        "Employee_RBT": False,
        "Employee_Other": False,
        "AttendeeInitials": ' '
    }

    # Generate a random 4 character string and add a random number 1 to 10 to the intials
    AttendeeInitials = ''.join(random.choices(string.ascii_lowercase, k=4)) + str(random.randrange(1, 10))
    # Randomly Select the boolean values:
    AttendeeDetails["Client"] = bool(random.getrandbits(1))
    if AttendeeDetails["Client"] == False:
        AttendeeDetails["Employee"] = True
        AttendeeDetails["Administrator"] = bool(random.getrandbits(1))
        if AttendeeDetails["Administrator"] == False:
            AttendeeDetails["Employee_SPOT"] = bool(random.getrandbits(1))
            if AttendeeDetails["Employee_SPOT"] == False:
                AttendeeDetails["Employee_BCBA"] = bool(random.getrandbits(1))
                if AttendeeDetails["Employee_BCBA"] == False:
                    AttendeeDetails["Employee_RBT"] = bool(random.getrandbits(1))
                else:
                    AttendeeDetails["Employee_Other"] = True
    else:
        AttendeeDetails["Employee"] = False
        AttendeeDetails["ABA_Earlychildhood"] = bool(random.getrandbits(1))
        if AttendeeDetails["ABA_Earlychildhood"] == False:
            AttendeeDetails["ABA_Teen"] = bool(random.getrandbits(1))
        else:
            AttendeeDetails["ABA_Teen"] = False

        AttendeeDetails["Occupational_Therapy"] = bool(random.getrandbits(1))
        AttendeeDetails["Speech_Therapy"] = bool(random.getrandbits(1))

    AttendeeDetails["AttendeeInitials"] = AttendeeInitials
    return AttendeeDetails

if __name__ == '__main__':
    create_attendees_and_events()
