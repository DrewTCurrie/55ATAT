import csv, os
from pathlib import Path
#Configuration path
APIPath = os.path.join('flaskServer', 'APIFuncs/')
ConfigurationPath = os.path.join(APIPath, 'databaseConfiguration')
#List all files in the configuration directory, these become the tables in the database
#Database will only support automatic bootstrapping for table names that fit the 
#MariaDB Data Management ERD table layout. These tables are:
    #Attendees, Administrators, CurrentAttendanceEvents, ArchivalEvents
#Creating more tables than this will not be processed into the system and data will not be retrieveable 
#Through the Admin UX sub-system

DatabaseTablesList = os.listdir(ConfigurationPath)
for dbTable in DatabaseTablesList: 
    if dbTable != "Attendees.csv":
        print("Error incorrect file name. Received: " + dbTable + " Expected Attndees.csv, Administrators.csv, or CurrentAttendanceEvents.csv")
    else:
        print("Database table name: " + Path(dbTable).stem)
        with open(os.path.join(ConfigurationPath, dbTable)) as databaseconfiguration:
            configuration = csv.reader(databaseconfiguration, delimiter = ',', quotechar='|')
            for row in configuration:
                for feild in row:
                    print(feild)
                    print("\n\r")