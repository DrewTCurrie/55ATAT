#Created 10/19/2024 Drew Currie
#Last editted: 10/19/2024 DC
#Garbage collector for left over files created during normal system operation
#This will check for old reports, old badges, old profile pictures and remove them.
#one function was written for each so that it would be modular. To call each in one function
#The collectGarbage function calls each in order. 
import os, sys

def RemoveOldReports():
    currentWorkingDirectory = os.path.abspath(os.getcwd())
    path = os.path.join(currentWorkingDirectory, 'flaskServer', 'xlsx/')
    ReportsList = os.listdir(path)
    print("Removing old reports located in " + path + ":")
    print(ReportsList)
    for report in ReportsList: 
        if report == ".gitkeep":
            print("Keeping " + report + "as it is not a report and is required for system operation.")
        else:   
            if os.path.isfile(path+report):
                os.remove(path+report)
        


def RemoveOldBadges():
    currentWorkingDirectory = os.path.abspath(os.getcwd())
    path = os.path.join(currentWorkingDirectory, 'flaskServer', 'static/')
    BadgeGenerationFileList = os.listdir(path)
    print("Removing old badges located in " + path + ":")
    print(BadgeGenerationFileList)
    for BadgeArtifact in BadgeGenerationFileList:
        if BadgeArtifact == "BadgeTemplates":
            print("Ignoring badge templates")
        elif BadgeArtifact == "audioFiles":
            print("Ignoring audioFiles directory. This will be cleaned up in a seperate function.")
        elif BadgeArtifact == ".gitignore":
            print("Keeping" + BadgeArtifact + "as it is not an artifact of creating a badege and is required for system operation.")
        else:
            if os.path.isfile(path+BadgeArtifact):
                os.remove(path+BadgeArtifact)

    
def RemoveOldProfilePictures():
    currentWorkingDirectory = os.path.abspath(os.getcwd())
    path = os.path.join(currentWorkingDirectory, 'flaskServer', 'profileImage/')
    ProfilePictureList = os.listdir(path)
    print("Removing old profile pictures located in " + path + ":")
    print(ProfilePictureList)
    for ProfilePicture in ProfilePictureList:
        if ProfilePicture == ".gitkeep":
            print("Keeping" + ProfilePicture + "as it is not an artifact of creating a badge and is required for system operation.")
        else:
            if os.path.isfile(path+ProfilePicture):
                os.remove(path+ProfilePicture)

def RemoveOldAudioFiles():
    currentWorkingDirectory = os.path.abspath(os.getcwd())
    path = os.path.join(currentWorkingDirectory, 'flaskServer', 'static', 'audioFiles/')
    audioFilesList = os.listdir(path)
    print("Removing old audio files in audioFiles folder")
    print(audioFilesList)
    for CustomAudio in audioFilesList:
        if CustomAudio == '0.mp3':
            print("Ignoring " + CustomAudio + "as it is a default audio file.")
        elif CustomAudio == '1.mp3':
            print("Ignoring " + CustomAudio + "as it is a default audio file.")
        elif CustomAudio == 'defaultFailureMaster.wav':
            print("Ignoring " + CustomAudio + "as it is a default audio file.")
        elif CustomAudio == 'defaultSuccessMaster.wav':
            print("Ignoring " + CustomAudio + "as it is a default audio file.")
        elif CustomAudio == '.gitkeep':
            print("Ignoring .gitkeep as it is not an audio file and is requried for system operation.")      
        else: 
            if os.path.isfile(path+CustomAudio):
                print("DELETING" + path+CustomAudio)
                os.remove(path+CustomAudio)

def CollectGarbage():
    RemoveOldReports()
    RemoveOldBadges()
    RemoveOldProfilePictures()
    



if __name__ == '__main__':
    sys.exit(RemoveOldAudioFiles())