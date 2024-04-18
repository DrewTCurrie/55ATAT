from APIFuncs import JSONHandler as jsonhandler

AttendeeJSON = jsonhandler.ReadJSON('NewAttendee.json')

#Now process the JSON:
print(AttendeeJSON['AttendeeDetails'][0]['Client'])