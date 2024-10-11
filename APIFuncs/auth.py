import hashlib
import os


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

# This function pulls 
def decrypt(stringToBeDecrypted):
    #Convert the hex string into bytes
    salt_and_hash = bytes.fromhex(stringToBeDecrypted)
    print(salt_and_hash)
    # Extract the salt (first 16 bytes)
    salt = salt_and_hash[:16]
    print(salt)
    hashedString = salt_and_hash[16:]
    print(hashedString)

#def createToken():
#def attemptLogin(username, password):


if __name__ == "__main__":
    testVal = 'Test'
    print(testVal)
    test = encrypt(testVal)
    print(test)
    decrypt(test)