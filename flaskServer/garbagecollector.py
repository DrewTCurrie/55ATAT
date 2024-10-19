import os, sys

def RemoveOldReports():
    path = "./xlsx/"
    ReportsList = os.listdir(path)
    print("Files located inside the " + path + "directory: ")
    print(ReportsList)

def RemoveOldBadges():
    


if __name__ == '__main__':
    sys.exit(RemoveOldReports())