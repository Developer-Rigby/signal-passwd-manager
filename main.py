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

    print("[Password Saved]")
    return mast_passwd

def userInput(): #DEBUGGED - WORKS - COULD BE BETTER
    id = 'Service: ' + input("Please specify the service: ")
    username = 'User: ' + input("Please state what username/email you use for this service: ")
    
    password = 0
    passwordRetry = 1
    while password != passwordRetry:
        password = 'Password: ' + getpass.getpass("Please input your password for this service: ")
        passwordRetry = 'Password: ' + getpass.getpass("Please retype your password: ")

        if password != passwordRetry:
            print("Those passwords did not match. Please try again.") 

    return id, username, password

#With this convertTuple
def convertTuple(tup):
        # initialize an empty string
    str = ''
    for item in tup:
        str = str + item + "\n"
        byteStr = str.encode("ascii")
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

def encryptedData(key, nonce):
    encryptedString = encryption(convertTuple(userInput()), key, nonce)
    return encryptedString

def decryptedData(ciphertext, key, nonce):
    decryptedBytes = decryption(ciphertext, key, nonce)
    decryptedString = str(decryptedBytes)
    data = decryptedString
    return data

def createCipherTXT(encryptedData):
    with open("encryptedTXT.txt", "wb") as ciphertext:
        ciphertext.write(encryptedData)

def debugging():
    nonce = os.urandom(12)
    key = seedPass()
    ciphertext = encryptedData(key, nonce)
    createCipherTXT(ciphertext)
    print("done encryption")
    print(decryptedData(ciphertext, key, nonce))
    print('nonce: ' + str(nonce))

    
#Procedure to create a TEMPORARY PLAINTEXT FILE
#def createTempPlainTXT(data): #POSSIBLE INSECURITY
#    with open("plaintextTEMP.txt", "wb") as plaintext:
#        plaintext.write(data)

#def encryptPlainTXT(): #NOT WORKING - I don't even think this is needed along with the creation of the plain text
#    toEncrypt = []
#    with open("plaintextTEMP.txt", "rb") as ciphertext:
#        ciphertext.read()
#        for byte in ciphertext:
#            x = encryption(char, seedPass())
#            toEncrypt.append(x)
#    return toEncrypt



def main():
    #This is the menu logo screen
    print(" .--.  _                    .-.                                                    .-.                                                ")
    print(": .--':_;                   : :                                                    : :                                                ")
    print("`. `. .-. .--. ,-.,-. .--.  : :    .---.  .--.   .--.  .--. .-..-..-. .--. .--.  .-' :  ,-.,-.,-. .--.  ,-.,-. .--.   .--.  .--. .--. ")
    print(" _`, :: :' .; :: ,. :' .; ; : :_   : .; `' .; ; `._-.'`._-.': `; `; :' .; :: ..'' .; :  : ,. ,. :' .; ; : ,. :' .; ; ' .; :' '_.': ..'")
    print("`.__.':_;`._. ;:_;:_;`.__,_;`.__;  : ._.'`.__,_;`.__.'`.__.'`.__.__.'`.__.':_;  `.__.'  :_;:_;:_;`.__,_;:_;:_;`.__,_;`._. ;`.__.':_;  ")
    print("          .-. :                    : :                                                                                .-. :           ")
    print("          `._.'                    :_;                                                                                `._.'           ")
    

    print("*Please select and option*")
    print("1. Create Database")
    print("2. Append Data")
    print("3. View Data")
    print("4. Delete Database")
    print("5. Exit...")


    option = input("Please select an option: ")
    match option:
        case "1":
            debugging()
        case "2":
            print(2)
        case "3":
            print(3)
        case "4":
            print(4)
        case "5":
            print("*Exiting*")
            exit()
        case _:
            print("Invalid. Try Again.")
        

main()




