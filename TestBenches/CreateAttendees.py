import sys
import os
import shutil
sys.path.append(os.path.join(sys.path[0], '../APIFuncs'))
import utils
import csv
import random
import string
import json

#Creating a test system to create new attendees randomly and populate them into a CSV to be read in
#to the databse for testing 

def CreateFakeAttendees(numberOfAttendees, Confirm):
    #Get number of attendees to create
    if(Confirm == "y" or "Y"):
        #Create a folder to dump all these JSONs into
        try:
            os.mkdir(os.path.join(sys.path[0], "AttendeeJSONFiles"))
        except:
            shutil.rmtree(os.path.join(sys.path[0], "AttendeeJSONFiles"))
            print("Removing old AttendeeJSONFiles")
            os.mkdir(os.path.join(sys.path[0], "AttendeeJSONFiles"))
            print("Creating empty AttendeeJSONFiles Folder")
        else:
            print("Created new AttendeeJSONFiles Folder")

        for ii in range(numberOfAttendees):


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
            AttendeeNumber = ii + 1
            JSONDumpFilePath =  os.path.join(sys.path[0], "AttendeeJSONFiles/TestJSON"+str(AttendeeNumber)+".json")
            with open(JSONDumpFilePath, "w") as outfile:
                outfile.write(jsonObject)
            #print("Attendee Num: " +str(AttendeeNumber) + "Created.")
    else:
          print("Not Confirmed. Aborting...")
          return(1)
