import os
import sys

import sqlalchemy
from flask import url_for
from pydub import AudioSegment

from APIFuncs import MariaDBapi as api, utils

#Pathing to audioFiles folder
sys.path.append(os.path.join(sys.path[0], '/audioFiles'))
defaultAudioFilePath = os.path.join('flaskServer', 'static', 'audioFiles', '0.mp3')
#--------------- Attendee Handling -----------------------------------------------------

#--------------- Message Handling -----------------------------------------------------
def getAttendeeMessage(attendeeID):
    # Create Sqlalchemy Session
    api.Base.metadata.create_all(api.engine)
    Session = sqlalchemy.orm.sessionmaker()
    Session.configure(bind=api.engine)
    Session = Session()
    #Query for attendee messasge
    query = Session.query(api.AttendeeMessage).filter_by(ID=attendeeID).first()
    if query is not None:
        message = query.Message
        Session.close()
        return message
    else:
        Session.close()
        return getDefaultMessage()

def setAttendeeMessage(attendeeID, message):
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
        newDefault = api.AttendeeMessage(ID=attendeeID, Message=message, audioPath=defaultAudioFilePath)
        Session.add(newDefault)
    Session.commit()
    Session.close()

#--------------- Audio Handling -----------------------------------------------------
def getAttendeeAudio(attendeeID):
    # Create Sqlalchemy Session
    api.Base.metadata.create_all(api.engine)
    Session = sqlalchemy.orm.sessionmaker()
    Session.configure(bind=api.engine)
    Session = Session()
    #Query for attendee messasge
    query = Session.query(api.AttendeeMessage).filter_by(ID=attendeeID).first()
    if query is not None:
        #Truncate file path for usage
        urlFullFilePath = query.audioPath
        urlFilePath = urlFullFilePath.replace(r"flaskServer\static"+"\\", "")
        #replace backslashes with forward slashes for url.
        urlFilePath = urlFilePath.replace('\\', '/')
        #Create a URL for the file path to service to flask server
        audioURL = url_for('static', filename=urlFilePath,_external=True)
        Session.close()
        return audioURL
    else:
        Session.close()
        return getDefaultSuccessAudio()




#--------------- Reset Handling -----------------------------------------------------
def resetAttendee(attendeeID):

    #Default Messages/Audio
    defaultMessage = "Welcome to PTC"
    defaultAudioPath = os.path.join('flaskServer', 'static', 'audioFiles', 'defaultSuccessMaster.wav')

    # Create Sqlalchemy Session
    api.Base.metadata.create_all(api.engine)
    Session = sqlalchemy.orm.sessionmaker()
    Session.configure(bind=api.engine)
    Session = Session()
    audioFilePath = convertAudio('0', defaultAudioPath)
    defaultEntry = Session.query(api.AttendeeMessage).filter_by(ID=attendeeID).first()
    if defaultEntry:
        defaultEntry.Message = defaultMessage
        defaultEntry.audioPath = audioFilePath
    else:
        newDefault = api.AttendeeMessage(ID=attendeeID,Message=defaultMessage,audioPath=audioFilePath)
        Session.add(newDefault)
    Session.commit()
    Session.close()

def setAttendeeAudio(attendeeID,audioFile):
    # Create Sqlalchemy Session
    api.Base.metadata.create_all(api.engine)
    Session = sqlalchemy.orm.sessionmaker()
    Session.configure(bind=api.engine)
    Session = Session()

    #Convert audio File into mp3, and rename to '0' (master entry)
    audioFilePath = convertAudio(attendeeID, audioFile)

    #Query for default entry, '0'
    query = Session.query(api.AttendeeMessage).filter_by(ID=attendeeID).first()
    #If this exists, edit the messages
    if query:
        query.audioPath = audioFilePath
    else:
        #If not, create a new ID=attendeeID entry.
        newDefault = api.AttendeeMessage(ID=attendeeID, Message='Welcome To PTC', audioPath=audioFilePath)
        Session.add(newDefault)
    Session.commit()
    Session.close()

#--------------- Default Handling -----------------------------------------------------

#--------------- Message Handling -----------------------------------------------------
def getDefaultMessage():
    # Create Sqlalchemy Session
    api.Base.metadata.create_all(api.engine)
    Session = sqlalchemy.orm.sessionmaker()
    Session.configure(bind=api.engine)
    Session = Session()

    #Query for default entry, '0'
    defaultEntry = Session.query(api.AttendeeMessage).filter_by(ID='0').first()
    if defaultEntry.Message:
        message = defaultEntry.Message
        Session.close()
        return message
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
        newDefault = api.AttendeeMessage(ID='0', Message=message, audioPath=defaultAudioFilePath)
        Session.add(newDefault)
    Session.commit()
    Session.close()

#--------------- Audio Handling -----------------------------------------------------

def setDefaultAudio(audioFile):
    # Create Sqlalchemy Session
    api.Base.metadata.create_all(api.engine)
    Session = sqlalchemy.orm.sessionmaker()
    Session.configure(bind=api.engine)
    Session = Session()

    #Convert audio File into mp3, and rename to '0' (master entry)
    audioFilePath = convertAudio('0', audioFile)

    #Query for default entry, '0'
    defaultEntry = Session.query(api.AttendeeMessage).filter_by(ID='0').first()
    #If this exists, edit the messages
    if defaultEntry:
        defaultEntry.audioPath = audioFilePath
    else:
        #If not, create a new ID='0' entry.
        newDefault = api.AttendeeMessage(ID='0', Message='Welcome to PTC', audioPath=audioFilePath)
        Session.add(newDefault)
    Session.commit()
    Session.close()

def getDefaultSuccessAudio():
    # Create Sqlalchemy Session
    api.Base.metadata.create_all(api.engine)
    Session = sqlalchemy.orm.sessionmaker()
    Session.configure(bind=api.engine)
    Session = Session()

    # Query for default entry, '0'
    defaultEntry = Session.query(api.AttendeeMessage).filter_by(ID='0').first()
    if defaultEntry:
        #Truncate file path for usage
        urlFullFilePath = defaultEntry.audioPath
        urlFilePath = urlFullFilePath.replace(r"flaskServer\static"+"\\", "")
        #replace backslashes with forward slashes for url.
        urlFilePath = urlFilePath.replace('\\', '/')
        #Create a URL for the file path to service to flask server
        audioURL = url_for('static', filename=urlFilePath,_external=True)
        Session.close()
        return audioURL
    else:
        Session.close()
        return "No Default Audio Found"


#--------------- Reset Handling -----------------------------------------------------

#This function resets the generic message back to default.
def resetDefaults():
    #Default Messages/Audio
    defaultMessage = "Welcome to PTC"
    defaultAudioPath = os.path.join('flaskServer', 'static', 'audioFiles', 'defaultSuccessMaster.wav')
    #flaskServer / static / audioFiles / defaultSuccessMaster.wav
    # Create Sqlalchemy Session
    api.Base.metadata.create_all(api.engine)
    Session = sqlalchemy.orm.sessionmaker()
    Session.configure(bind=api.engine)
    Session = Session()
    audioFilePath = convertAudio('0', defaultAudioPath)
    defaultEntry = Session.query(api.AttendeeMessage).filter_by(ID='0').first()
    if defaultEntry:
        defaultEntry.Message = defaultMessage
        defaultEntry.audioPath = audioFilePath
    else:
        newDefault = api.AttendeeMessage(ID='0', Message=defaultMessage, audioPath=defaultAudioPath)
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
    AudioFilePath = os.path.join('flaskServer', 'static', 'audioFiles', new_filename)
    #Read File from File path.
    audioToConvert = AudioSegment.from_file(audioFile)
    #Create a new file for output
    file = open(AudioFilePath, 'w+')
    #Export audio as mp3
    audioToConvert.export(AudioFilePath, format="mp3")
    file.close()

    return AudioFilePath


if __name__ == '__main__':
    defaultAudioPath = os.path.join('..','flaskServer', 'static', 'audioFiles', 'defaultSuccessMaster.wav')
    audioFilePath = convertAudio('0', defaultAudioPath)
    print(audioFilePath)