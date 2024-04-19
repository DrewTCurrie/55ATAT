import sys
import os
sys.path.append(os.path.join(sys.path[0], '../APIFuncs'))
import utils
import csv
import random
import string
import json

#Creating a test system to create new attendees randomly and populate them into a CSV to be read in
#to the databse for testing 

def main():
    #Get number of attendees to create
    numberOfAttendees = int(input("How many Attendees to create?"))
    Confirm = input("Confirm" + str(numberOfAttendees) + "? y/n")
    if(Confirm == "y" or "Y"):
        #Create a folder to dump all these JSONs into
        os.mkdir(os.path.join(sys.path[0], "AttendeeJSONFiles"))
        #Create python dictionary to hold all the randomly generated details for the imaginary attendee
        AttendeeDetails = {
            "Client" : False,
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


        #Generate a random 4 character string and add a random number 1 to 10 to the intials 
        AttendeeInitials =''.join(random.choices(string.ascii_lowercase, k = 4)) + str(random.randrange(1,10))
        #Randomly Select the boolean values:
        AttendeeDetails["Client"] = bool(random.getrandbits(1))
        if AttendeeDetails["Client"] == False:
            AttendeeDetails["Employee"] = True
            AttendeeDetails["Administrator"] = bool(random.getrandbits(1))
            if AttendeeDetails["Administrator"] == False:
                AttendeeDetails["Employee_SPOT"]  = bool(random.getrandbits(1))
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

        jsonObject = json.dumps(AttendeeDetails, indent = 4)

        with open("AttendeeJSONFiles/TestJSON.json", "w") as outfile:
            outfile.write(jsonObject)
        print(jsonObject)
    else:
          return(1)
if __name__ == '__main__':
        main()
    
