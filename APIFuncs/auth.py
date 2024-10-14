import hashlib
import os

import sqlalchemy

from APIFuncs import MariaDBapi as api, utils


# This function takes in a string, then salts, encrypts and appends
# the salt to the string for decryption.
def encrypt(stringToBeEncrypted):
    # Generate a 16-byte salt
    salt = os.urandom(16)
    # Concatenate with string to be encrypted
    salted_input = salt + stringToBeEncrypted.encode('utf-8')
    #Hash the salted input
    hashedString = hashlib.sha256(salted_input).digest()
    # Add salt to front for reference in decryption
    salt_and_hash = salt + hashedString
    #return as hex string for entry in DB.
    return salt_and_hash.hex()

def adminLogin(username, inputPassword):
    if username == 'admin' and inputPassword == 'admin':
        return True
    else:
        return False

#This function attempts to check the login of a user, and returns true if it is valid
def attemptLogin(username, inputPassword):
    # Try global password
    if adminLogin(username, inputPassword):
        return {"Success": True, "Message": 'Login Successful', "adminInitials":"GlobalAdmin"}
    # Create Sql Alchemy Session
    Session = sqlalchemy.orm.sessionmaker()
    Session.configure(bind=api.engine)
    Session = Session()
    #Query Database for username + hashedPassword
    query = Session.query(api.Administrator).filter_by(UserName=username).first()
    if query is None:
        return {"Success": False, "Message": 'Username not Found'}
    else:
        #Parse dbPassword for salt and rest of password
        dbPassword = bytes.fromhex(query.Password)
        dbSalt = dbPassword[:16]
        dbHashedPassword = dbPassword[16:]
    #Append Salt to inputPassword
    saltedInput = dbSalt + inputPassword.encode('utf-8')
    hashedInput = hashlib.sha256(saltedInput).digest()

    #Close Session
    Session.close()

    if hashedInput == dbHashedPassword:
        #Get Attendee Data from Adminsitrator Username
        adminID = utils.getIDFromAdministrator(username)
        # Get AdminInitials and add it to response
        adminInfo = utils.getAttendee(adminID)
        return {"Success": True, "Message": 'Login Successful',"adminInitials": adminInfo.AttendeeInitials}
    else:
        return {"Success": False, "Message": 'Incorrect password'}



if __name__ == "__main__":
    testVal = 'Test'
    print(len(testVal))
    print(testVal)
    test = encrypt(testVal)
    print(test)
    print(len(test))