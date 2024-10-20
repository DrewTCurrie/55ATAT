import json
import datetime

def ReadJSON(FILEPATH):
    #Open JSON file
    OpenJSON = open(FILEPATH)
    data = json.load(OpenJSON)
    return(data)


def PopulateJSONReport(FILEPATH, ATTENDANCE_DATA):
    #Crate a JSON at FILEPATH 
    #Populate Class Object with all attendance events from ATTENDANCE_DATA
    Event = AttendanceReport(ATTENDANCE_DATA.EventUUID, ATTENDANCE_DATA.ID, ATTENDANCE_DATA.AttendeeInitials, 
                             ATTENDANCE_DATA.Timestamp, ATTENDANCE_DATA.Absent, ATTENDANCE_DATA.TIL_Violation,
                             ATTENDANCE_DATA.AdminInitials, ATTENDANCE_DATA.Comment)
    with open(FILEPATH, "a") as Report:   

        json.dump(Event.__dict__, Report, indent = 4)

# This function converts a query into json generically.
def queryToJSON(query):
    #parses each row for column name, and their values.
    def rowToDict(row):
        return {column.name: getattr(row, column.name) for column in row.__table__.columns}

    jsonQuery = [rowToDict(row) for row in query]
    return json.dumps(jsonQuery)

class AttendanceReport:
    def __init__(self, EventID, AttendeeID, AttendeeInitials, Timestamp, Absent, TIL_Violation, AdminInitials, Comment):
        self.EventID = EventID
        self.ID = AttendeeID
        self.AttendeeInitials = AttendeeInitials
        self.Timestamp = Timestamp.strftime("%y-%m-%d-%h-%m-%s")
        self.Absent = Absent
        self.TIL_Violation = TIL_Violation
        self.AdminInitials = AdminInitials
        self.Comment = Comment