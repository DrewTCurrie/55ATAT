import json

def ReadJSON(FILEPATH):
    #Open JSON file
    OpenJSON = open(FILEPATH)
    data = json.load(OpenJSON)
    return(data)

