import os
import sys

import sqlalchemy
from pydub import AudioSegment

from APIFuncs import MariaDBapi as api, utils

#Pathing to audioFiles folder
sys.path.append(os.path.join(sys.path[0], '/audioFiles'))
image_folder = 'flaskServer/static/audioFiles'

#--------------- Attendee Handling -----------------------------------------------------

# def setAttendeeMessage(attendeeID):
#
def getAttendeeMessage(attendeeInitials):
    #Get Attendee Initials
    attendeeID = utils.getIDfromInitials(attendeeInitials)
    # Create Sqlalchemy Session
    api.Base.metadata.create_all(api.engine)
    Session = sqlalchemy.orm.sessionmaker()
    Session.configure(bind=api.engine)
    Session = Session()
    #Query for attendee messasge
    query = Session.query(api.AttendeeMessage).filter_by(ID=attendeeID).first()
    if query is not None:
        return query.Message
    else:
        return getDefaultMessage()

def setAttendeeMessage(attendeeInitials, message):
    #Get Attendee Initials
    attendeeID = utils.getIDfromInitials(attendeeInitials)
    # Create Sqlalchemy Session
    api.Base.metadata.create_all(api.engine)
    Session = sqlalchemy.orm.sessionmaker()
    Session.configure(bind=api.engine)
    Session = Session()
    #Query for attendee messasge
    query = Session.query(api.AttendeeMessage).filter_by(ID=attendeeID).first()
    #If this exists, edit the messages
    if query:
        query.Message = message
    else:
        #If not, create a new ID='0' entry.
        newDefault = api.AttendeeMessage(ID=attendeeID, Message=message, audioPath='')
        Session.add(newDefault)
    Session.commit()
    Session.close()


def resetAttendee(attendeeInitials):
    #Get Attendee Initials
    attendeeID = utils.getIDfromInitials(attendeeInitials)

    #Default Messages/Audio
    defaultMessage = "Welcome to PTC"
    defaultAudioPath = os.path.join('flaskServer', 'static', 'defaultSuccessMaster.wav')

    # Create Sqlalchemy Session
    api.Base.metadata.create_all(api.engine)
    Session = sqlalchemy.orm.sessionmaker()
    Session.configure(bind=api.engine)
    Session = Session()

    defaultEntry = Session.query(api.AttendeeMessage).filter_by(ID=attendeeID).first()
    if defaultEntry:
        defaultEntry.Message = defaultMessage
        defaultEntry.audioPath = defaultAudioPath
    else:
        newDefault = api.AttendeeMessage(ID=attendeeID,Message=defaultMessage,audioPath=defaultAudioPath)
        Session.add(newDefault)
    Session.commit()
    Session.close()

#--------------- Default Handling -----------------------------------------------------

def getDefaultMessage():
    # Create Sqlalchemy Session
    api.Base.metadata.create_all(api.engine)
    Session = sqlalchemy.orm.sessionmaker()
    Session.configure(bind=api.engine)
    Session = Session()

    #Query for default entry, '0'
    defaultEntry = Session.query(api.AttendeeMessage).filter_by(ID='0').first()
    Session.close()
    if defaultEntry.Message:
        return defaultEntry.Message
    else:
        return "No Message Found"
def setDefaultMessage(message):
    # Create Sqlalchemy Session
    api.Base.metadata.create_all(api.engine)
    Session = sqlalchemy.orm.sessionmaker()
    Session.configure(bind=api.engine)
    Session = Session()

    #Query for default entry, '0'
    defaultEntry = Session.query(api.AttendeeMessage).filter_by(ID='0').first()
    #If this exists, edit the messages
    if defaultEntry:
        defaultEntry.Message = message
    else:
        #If not, create a new ID='0' entry.
        newDefault = api.AttendeeMessage(ID='0', Message=message, audioPath='')
        Session.add(newDefault)
    Session.commit()
    Session.close()

#def setDefaultAudio(audioFile):


#This function resets the generic message back to default.
def resetDefaults():
    #Default Messages/Audio
    defaultMessage = "Welcome to PTC"
    defaultAudioPath = os.path.join('flaskServer', 'static', 'defaultSuccessMaster.wav')

    # Create Sqlalchemy Session
    api.Base.metadata.create_all(api.engine)
    Session = sqlalchemy.orm.sessionmaker()
    Session.configure(bind=api.engine)
    Session = Session()

    defaultEntry = Session.query(api.AttendeeMessage).filter_by(ID='0').first()
    if defaultEntry:
        defaultEntry.Message = defaultMessage
        defaultEntry.audioPath = defaultAudioPath
    else:
        newDefault = api.AttendeeMessage(ID='0',Message=defaultMessage,audioPath=defaultAudioPath)
        Session.add(newDefault)
    Session.commit()
    Session.close()

#--------------- Audio File Conversion -----------------------------------------------------
# This ensures that all audio files are of the same type.

#This function converts and saves input audio into an MP3 for usage in the system based on ID
#NOTE: This requires ffmpeg to be installed to run, use (sudo apt-get install ffmpeg) on Linux

def convertAudio(attendeeID,audioFile):
    #Create an output filepath using attendeeID
    # Create file name with UserID
    file_extension = '.mp3'  # Get the file extension
    new_filename = f"{attendeeID}{file_extension}"
    #Assign file path to staic folder
    AudioFilePath = os.path.join('flaskServer', 'static', new_filename)
    #Read File from File path.
    audioToConvert = AudioSegment.from_file(audioFile)
    #Export audio as mp3
    audioToConvert.export(AudioFilePath, format="mp3")


if __name__ == '__main__':
    defaultAudioPath = "flaskServer/static/audioFiles/defaultSuccessMaster.wav"
    print('Messages Test')
    print(setDefaultMessage('Test Test Test'))
    print(getDefaultMessage())
    resetDefaults()
    print(getDefaultMessage())