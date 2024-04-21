import sys
import os
sys.path.append(os.path.join(sys.path[0], '../APIFuncs'))
import utils
import CreateAttendees as CA
import time

def main():
    numberOfAttendees = int(input("How many Attendees to create?:  "))
    Confirm = input("Confirm creating " + str(numberOfAttendees) + " number of new attendees? y/n:  ")
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
            print("Successfully wrote Attendee: " +str(AttendeeNumber) + str(" to Attendee table"))
if __name__ == '__main__':
    sys.exit(main())