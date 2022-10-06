from abc import abstractstaticmethod
from distutils.log import debug
from lib2to3.pytree import convert
from pydoc import doc
from random import seed
from Crypto.Cipher import ChaCha20
import string
import os
import getpass

#Standard user password creation. As per usual, you have to retype your password incase you mistyped it wrong the first.
def masterPassword(): #DEBUGGED - WORKS
    mast_passwd = 0
    mast_passwdRetry = 1 #specifying that these two are different

    print("Although there are no limits on what your password can be, for the best security make sure to use capitals, numbers and symbols.")

    while mast_passwd != mast_passwdRetry:
        mast_passwd = getpass.getpass("Please type a password: ") #using getpass to hide the user input
        mast_passwdRetry = getpass.getpass("Please retype your password: ")
        if mast_passwd != mast_passwdRetry:
            print("Those passwords did not match. Please try again.")

    return mast_passwd

def userInput(): #DEBUGGED - WORKS - RETURNS TUPLE ARRAYS
    id = []
    username = []
    passwordS = []

    serviceAmountString = input("How many services are you writing?:  ")
    serviceAmount = int(serviceAmountString)
    interval = 0 #Defining a c++ style for loop in python. I have never done this and I wish that it was more like c++
    while interval < serviceAmount:

        id.append('Service: ' + input("Please specify the service: "))
        username.append('User: ' + input("Please state what username/email you use for this service: "))
        
        password = 0
        passwordRetry = 1
        while password != passwordRetry:
            password = 'Password: ' + getpass.getpass("Please input your password for this service: ")
            passwordRetry = 'Password: ' + getpass.getpass("Please retype your password: ")

            if password == passwordRetry:
                passwordS.append(password + '\n')

            if password != passwordRetry:
                print("Those passwords did not match. Please try again.") 
        interval = interval + 1

    serviceTuples = zip(id, username, passwordS)
    serviceLists = [item for t in serviceTuples for item in t]
    return serviceLists

def convertList(list):
    str = ''
    for elem in list:
        str = str + elem + '\n'
        byteStr = str.encode('ascii')
    return byteStr

#function that uses chacha20 to encrypt
def encryption(message, key, nonce):
    cipher = ChaCha20.new(key = key, nonce = nonce)
    ciphertext = cipher.encrypt(message)
    return ciphertext

def decryption(message, key, nonce):
    cipher = ChaCha20.new(key = key, nonce = nonce)
    plaintext = cipher.decrypt(message)
    return plaintext

#Function that converts ASCII to their corresponding Decimal counterpart.
def ASCIItoDECIMAL(toconvert): #DEBUGGED - WORKING
    convertedArray = []
    for char in toconvert:
        convertedArray.append(ord(char)) #splits a string and converts them into an array of decimal
    
    convertedString = ' '.join([str(elem) for elem in convertedArray]) #converts the array to a string

    return convertedString

#Function that generates a key from a string (Password). It is reversable.
def seedPass(): #DEBUGGED - WORKING - COULD BE BETTER
    randomNumber = 81776850632311620355058304162600 #literally just a random number
    stringDecimalPass = ASCIItoDECIMAL(masterPassword())
    stringDecimalPass = stringDecimalPass.replace(' ', '') #replaces all spaces with no spaces.
    decimalPass = int(stringDecimalPass)

    stringKey = randomNumber ^ decimalPass
    key = stringKey.to_bytes(32, 'big')

    return key
    

def encryptedData(key, nonce): #DEBUGGED - WORKS
    #long process that usees above functions to take user inputted data and return encrypted data
    serviceInput = userInput()
    inputToList = convertList(serviceInput)
    encryptedUserData = encryption(inputToList, key, nonce)

    return encryptedUserData

def decryptedData(ciphertext, key, nonce): #DEBUGGED - WORKS
    decryptedBytes = decryption(ciphertext, key, nonce)
    decryptedString = decryptedBytes.decode("UTF-8")
    return decryptedString

#creates a txt with encrypted hexadecimal that cannot be read without the key/password
def createCipherTXT(encryptedData): #DEBUGGED - WORKS - Could be better
    with open("encryptedTXT.txt", "wb") as ciphertext:
        ciphertext.write(encryptedData)

def debugging():
    print(userInput())


#Although it's not generally secure to reuse a nonce (you should really never do it especcially in cloud based situations), we will do it here as everything is client side.
#Still, never do it. Replay attacks can still occur especially if the user uses both the same key and nonce. I'll only be keeping it until I figure out a way to not save the nonce.
def createDatabase(): #SECURITY VULNERABILITY
    nonce = b'K\x8b\xa9\xf2\xfc\x06\x9br\xdb\xcb\xaaH'
    key = seedPass()
    ciphertext = encryptedData(key, nonce)
    createCipherTXT(ciphertext)
    print("[Saved - Encryption complete]")

def decryptDatabase():
    nonce = b'K\x8b\xa9\xf2\xfc\x06\x9br\xdb\xcb\xaaH'
    key = seedPass()
    with open("encryptedTXT.txt", "rb") as ciphertext:
        jargon = ciphertext.read()
        print(decryptedData(jargon, key, nonce))

def deleteDataBase():
    if os.path.exists("encryptedTXT.txt"):
        inputDeleteDatabase = input("Delete this database? y/n: ")
        while inputDeleteDatabase != "y" or "n":
            if inputDeleteDatabase == "y":
                os.remove("encryptedTXT.txt")
                print("##########################")
                menuScreen()
            elif inputDeleteDatabase == "n":
                print("[Database not deleted]")
                return 0
            else:
                inputDeleteDatabase = input("Invalid. Please try again: ")
    else:
        print("Database does not exist.")

def splashScreen():
    #This is the menu logo screen
    print(" .--.  _                    .-.                                                    .-.                                                ")
    print(": .--':_;                   : :                                                    : :                                                ")
    print("`. `. .-. .--. ,-.,-. .--.  : :    .---.  .--.   .--.  .--. .-..-..-. .--. .--.  .-' :  ,-.,-.,-. .--.  ,-.,-. .--.   .--.  .--. .--. ")
    print(" _`, :: :' .; :: ,. :' .; ; : :_   : .; `' .; ; `._-.'`._-.': `; `; :' .; :: ..'' .; :  : ,. ,. :' .; ; : ,. :' .; ; ' .; :' '_.': ..'")
    print("`.__.':_;`._. ;:_;:_;`.__,_;`.__;  : ._.'`.__,_;`.__.'`.__.'`.__.__.'`.__.':_;  `.__.'  :_;:_;:_;`.__,_;:_;:_;`.__,_;`._. ;`.__.':_;  ")
    print("          .-. :                    : :                                                                                .-. :           ")
    print("          `._.'                    :_;                                                                                `._.'           ")

def menuScreen():
    print("*Please select and option*")
    print("1. Create Database")
    print("2. Append Data")
    print("3. View Data")
    print("4. Delete Database")
    print("5. Exit...")
    print("6. **DEBUGGING - DEV ONLY**")

    option = input("Please select an option: ")
    match option:
        case "1":
            createDatabase()
        case "2":
            print(2)
        case "3":
            decryptDatabase()
        case "4":
            deleteDataBase()
        case "5":
            print("*Exiting Program*")
            exit()
        case "6":
            debugging()
        case _:
            print("Invalid. Try Again.")
            menuScreen()
        
def main():
    splashScreen()
    menuScreen()

main()




