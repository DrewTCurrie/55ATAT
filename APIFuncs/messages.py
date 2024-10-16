import os

import sqlalchemy
from APIFuncs import MariaDBapi as api, utils


# def setAttendeeMessage(attendeeID):
#
# def getAttendeeMessage(attendeeID):
#


#--------------- Default Handling -----------------------------------------------------

# def getDefaultMessage():
#
#def setDefaultMessage(message):

def setDefaultAudio(audioFile):


#This function resets the generic message back to default.
def resetDefaults():
    defaultMessage = "Welcome to PTC"
    defaultAudioPath = os.path.join('flaskServer', 'static', 'defaultSuccess.wav')
    api.AttendeeMessage(ID='0',Message=defaultMessage,audioPath=)

#--------------- Audio File Conversion -----------------------------------------------------
# This ensures that all audio files are of the same type.

def convertAudio

if __name__ == '__main__':
    defaultAudioPath = os.path.join('flaskServer', 'static', 'defaultSuccess.wav')
    print('Messages Test')