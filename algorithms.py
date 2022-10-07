from Crypto.Cipher import ChaCha20
from lib2to3.pytree import convert

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
def createCipherTXT(encryptedData, userDBname): #DEBUGGED - WORKS - Could be better
    save_path = './databases/' #Telling the program to save to this directory
    completefilename = os.path.join(save_path, userDBname + ".txt")
    with open(completefilename, "wb") as ciphertext:
        ciphertext.write(encryptedData)


def createDatabase(): #SECURITY VULNERABILITY
    userDBname = input("What would you like to name this database: ")
    nonce = b'K\x8b\xa9\xf2\xfc\x06\x9br\xdb\xcb\xaaH'
    key = seedPass()
    ciphertext = encryptedData(key, nonce)
    createCipherTXT(ciphertext, userDBname)
    print("[Saved - Encryption complete]")

def decryptDatabase():
    nonce = b'K\x8b\xa9\xf2\xfc\x06\x9br\xdb\xcb\xaaH'
    key = seedPass()
    with open("encryptedTXT.txt", "rb") as ciphertext:
        jargon = ciphertext.read()
        print(decryptedData(jargon, key, nonce))

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
    print("2. Append Data")
    print("3. View Databases")
    print("4. View Data")
    print("5. Delete Database")
    print("6. Exit...")

    option = input("Please select an option: ")
    match option:
        case "1":
            createDatabase()
        case "2":
            print(2)
        case "3":
            print(0)
        case "4":
            decryptDatabase()
        case "5":
            userDBname = input("What database would you like to delete: ")
            pathName = './databases/'
            full_path = os.path.join(pathName, userDBname + '.txt')
            deleteDataBase(full_path)
        case "6":
            print("*Exiting Program*")
            exit()
        case _:
            print("Invalid. Try Again.")
            menuScreen()