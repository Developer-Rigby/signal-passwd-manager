from Crypto.Cipher import ChaCha20
from lib2to3.pytree import convert
import glob
from numpy import save
from user_inputs import *
import string
import os

#function that uses chacha20 to encrypt
def encryption(message, key, nonce):
    cipher = ChaCha20.new(key = key, nonce = nonce)
    ciphertext = cipher.encrypt(message)
    return ciphertext

def decryption(message, key, nonce):
    cipher = ChaCha20.new(key = key, nonce = nonce)
    plaintext = cipher.decrypt(message)
    return plaintext

#Function that generates a key from a string (Password). It is reversable.
def seedPass(masterpass): #DEBUGGED - WORKING - COULD BE BETTER
    randomNumber = 81776850632311620355058304162600 #literally just a random number
    stringDecimalPass = ASCIItoDECIMAL(masterpass)
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
def createCipherTXT(encryptedData, userDBname): #DEBUGGED - WORKS - Could be better
    save_path = './databases/' #Telling the program to save to this directory
    completefilename = os.path.join(save_path, userDBname + ".txt")
    with open(completefilename, "wb") as ciphertext:
        ciphertext.write(encryptedData)


def createDatabase(): #SECURITY VULNERABILITY
    userDBname = input("What would you like to name this database: ")
    nonce = b'K\x8b\xa9\xf2\xfc\x06\x9br\xdb\xcb\xaaH'
    key = seedPass(masterPassword())
    ciphertext = encryptedData(key, nonce)
    createCipherTXT(ciphertext, userDBname)
    print("[Saved - Encryption complete]")

def decryptDatabase(selectedDatabase):
    nonce = b'K\x8b\xa9\xf2\xfc\x06\x9br\xdb\xcb\xaaH'
    enterPass = getpass.getpass("Please enter your master password: ")
    try:
        key = seedPass(enterPass)
        save_path = './databases/'
        completefilename = os.path.join(save_path, selectedDatabase + '.txt')
        if os.path.exists(completefilename):
            with open(completefilename, "rb") as ciphertext:
                jargon = ciphertext.read()
                print(decryptedData(jargon, key, nonce))
        else:
            print("File path does not exist. Please try again")
            menuScreen()
    except UnicodeDecodeError: #If the program cannot decode because the key was wrong, this output is displayed
        print("***Invalid Password***")
        print("###############")
        menuScreen()

def deleteDataBase(userDBname):
    if os.path.exists(userDBname):
        inputDeleteDatabase = input("Delete this database? y/n: ")
        while inputDeleteDatabase != "y" or "n":
            if inputDeleteDatabase == "y":
                os.remove(userDBname)
                print("##########################")
                menuScreen()
            elif inputDeleteDatabase == "n":
                print("[Database not deleted]")
                return 0
            else:
                inputDeleteDatabase = input("Invalid. Please try again: ")
    else:
        print("Database does not exist.")

def printDatabases():
    print(glob.glob("./databases/*"))

#I put this here to avoid spaghetti; Even though there is still spaghetti
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
    print("2. Print Available Databases")
    print("3. View Data")
    print("4. Delete Database")
    print("5. Exit...")

    option = input("Please select an option: ")
    match option:
        case "1":
            createDatabase()
        case "2":
            printDatabases()
            print("################")
            menuScreen()
        case "3":
            selectedDatabase = input("Please enter the database you would like to view: ")
            decryptDatabase(selectedDatabase)
            print("###############")
            menuScreen()
        case "4":
            userDBname = input("What database would you like to delete: ")
            pathName = './databases/'
            full_path = os.path.join(pathName, userDBname + '.txt')
            deleteDataBase(full_path)
        case "5":
            print("*Exiting Program*")
            exit()
        case _:
            print("Invalid. Try Again.")
            menuScreen()