from abc import abstractstaticmethod
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

def userInput(): #DEBUGGED - WORKS
    id = input("Please specify the service: ")
    username = input("Please state what username/email you use for this service: ")
    
    password = 0
    passwordRetry = 1
    while password != passwordRetry:
        password = getpass.getpass("Please input your password for this service: ")
        passwordRetry = getpass.getpass("Please retype your password: ")

        if password != passwordRetry:
            print("Those passwords did not match. Please try again.")

#turning strings into bytes
    idByte = bytes(id, 'ascii')
    usernameByte = bytes(username, 'ascii')
    passwordByte = bytes(password, 'ascii')    

    return idByte, usernameByte, passwordByte

#function that uses chacha20 to encrypt
def encryption(message, key):
    cipher = ChaCha20.new(key = key)
    ciphertext = cipher.encrypt(message)
    return ciphertext

#Function that converts ASCII to their corresponding Decimal counterpart.
def ASCIItoDECIMAL(toconvert): #DEBUGGED - WORKING
    convertedArray = []
    for char in toconvert:
        convertedArray.append(ord(char)) #splits a string and converts them into an array of decimal
    
    convertedString = ' '.join([str(elem) for elem in convertedArray]) #converts the array to a string

    return convertedString

#Function that generates a key from a string (Password). It is reversable.
def seedPass(): #NOT WORKING - TO FIX ASAP
    randomNumber = 81776850632311620355058304162600 #literally just a random number
    stringDecimalPass = ASCIItoDECIMAL(masterPassword())

    key = randomNumber ^ decimalPass

    return key
#Procedure to create a TEMPORARY PLAINTEXT FILE
def createTempPlainTXT(data): #POSSIBLE INSECURITY
    with open("plaintextTEMP.txt", "w") as plaintext:
        plaintext.write(data)

print(seedPass())







