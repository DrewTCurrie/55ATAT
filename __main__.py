import sys
import os
#sys.path.append(os.path.join(sys.path[0], 'APIFuncs'))
#sys.path.insert(0, '/APIFuncs/')
import utils
import time


def main():
    action = 10
    while action != 0:
        action = int(input("Press 1 for NewAttendee, 2 for NewAttandanceEvent. Press 0 for close."))
        if(action == 2):
            print("Action Selected: New Attendance Event")
            UserID = input("Enter User ID: ")
            Result = utils.NewAttendanceEvent(UserID)
            if(Result == 400):
                print("Could not write to database.")
            else:
                print("successfully written to database")
        elif(action == 1):
            print("Action Selected: New Attendee Creation")
            print("Reading test JSON in directory")
            utils.NewAttendee()
        elif(action == 0):
             break
        else:
             print("Unknown Command. \n")
        time.sleep(2)

        
if __name__ == '__main__':

        sys.exit(main())