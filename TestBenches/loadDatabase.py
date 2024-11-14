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
sys.path.append(os.path.join(sys.path[0], '/home/55ATAT/55ATAT/flaskServer'))

from APIFuncs import MariaDBapi as api
from APIFuncs import utils


#Create list of possible reasons for being absent

absent_reasons = [
    "Client reported illness or medical emergency.",
    "Client had a family emergency or crisis.",
    "Client was scheduled for surgery or a procedure.",
    "Client experienced personal health issues.",
    "Client faced unexpected transportation problems.",
    "Client was caring for a sick family member.",
    "Client attended a funeral or memorial service.",
    "Client had vacation or travel plans.",
    "Client took a mental health day.",
    "Client's child had a school event or emergency.",
    "Client encountered weather-related issues, such as snow.",
    "Client had a job interview or career opportunity.",
    "Client was involved in moving or relocation tasks.",
    "Client experienced a home repair emergency.",
    "Client had a court appearance or legal obligations.",
    "Client attended a professional development workshop.",
    "Client had volunteer commitments or events.",
    "Client was at a dental appointment or treatment.",
    "Client was grocery shopping for the family.",
    "Client observed a religious holiday."
]

til_reasons = [
    "Client arrived late due to traffic congestion.",
    "Client had a last-minute appointment that ran over time.",
    "Client encountered unexpected public transportation delays.",
    "Client was delayed by a family emergency.",
    "Client's previous appointment ran longer than expected.",
    "Client had difficulty finding parking.",
    "Client experienced personal health issues that delayed their arrival.",
    "Client was unable to locate the clinic on time.",
    "Client had to assist a family member before coming.",
    "Client miscalculated travel time and arrived late.",
    "Client needed to pick up a prescription before the appointment.",
    "Client was involved in a prior commitment that ran over.",
    "Client experienced issues with their vehicle.",
    "Client received a call or message that required immediate attention.",
    "Client left early due to feeling unwell during the session.",
    "Client had a childcare issue that required them to leave.",
    "Client needed to attend to a work-related emergency.",
    "Client received an unexpected phone call during the session.",
    "Client felt overwhelmed and decided to leave early.",
    "Client had to meet someone urgently after the appointment.",
    "Client experienced a personal crisis that prompted an early exit."
]



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
        #Make 30 attendance events for each attendee starting from today
        for i in range(31):
            date = datetime.datetime.now()
            mst = pytz.timezone('America/Denver')
            date = mst.localize(date)
            comment = 'N/A' #Set default comment
            absent = False #Set default value
            tilViolation = False #Set default value

            #Make some randomly TAIL
            tailViolation = bool(random.getrandbits(1))
            if tailViolation:
                #randomly make some absents
                absent = bool(random.getrandbits(1))
                if absent:
                    comment = random.choice(absent_reasons)
                elif tailViolation:
                    comment = random.choice(til_reasons)
                    tilViolation = True
                else:
                    comment = 'N/A'

            NewAttendanceEvent = api.AttendanceEvent(EventUUID=uuid.uuid4(), ID=newUserID, AttendeeInitials=AttendeeJSON['AttendeeInitials'],
                                                     Timestamp=(date - datetime.timedelta(days=i)), Absent=absent, TIL_Violation=tilViolation,
                                                     AdminInitials="N/A", Comment=comment)
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
