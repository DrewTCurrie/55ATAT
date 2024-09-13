import os
import sys
sys.path.append(os.path.join(sys.path[0], '../APIFuncs'))
from APIFuncs import utils

def loadAttendees():
    directory = 'AttendeeJSONFiles/'
    file_paths = [os.path.join(directory,file) for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
    for file in file_paths:

        utils.NewAttendee(file)

if __name__ == '__main__':
    loadAttendees()
