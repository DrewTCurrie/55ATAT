import os, sys

def RemoveOldReports():
    path = "./xlsx/"
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
    path ="./static/"
    BadgeGenerationFileList = os.listdir(path)
    print("Removing old badges located in " + path + ":")
    print(BadgeGenerationFileList)
    for BadgeArtifact in BadgeGenerationFileList:
        if BadgeArtifact == "BadgeTemplates":
            print("Ignoring badge templates")
        elif BadgeArtifact == ".gitignore":
            print("Keeping" + BadgeArtifact + "as it is not an artifact of creating a badege and is required for system operation.")
        else:
            if os.path.isfile(path+BadgeArtifact):
                os.remove(path+BadgeArtifact)

    
def RemoveOldProfilePictures():
    path = "./profileImage/"
    ProfilePictureList = os.listdir(path)
    print("Removing old profile pictures located in " + path + ":")
    print(ProfilePictureList)
    for ProfilePicture in ProfilePictureList:
        if ProfilePicture == ".gitkeep":
            print("Keeping" + ProfilePicture + "as it is not an artifact of creating a badege and is required for system operation.")
        else:
            if os.path.isfile(path+ProfilePicture):
                os.remove(path+ProfilePicture)


if __name__ == '__main__':
    sys.exit(RemoveOldProfilePictures())