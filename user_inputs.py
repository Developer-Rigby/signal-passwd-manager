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

#Function that converts ASCII to their corresponding Decimal counterpart.
def ASCIItoDECIMAL(toconvert): #DEBUGGED - WORKING
    convertedArray = []
    for char in toconvert:
        convertedArray.append(ord(char)) #splits a string and converts them into an array of decimal
    
    convertedString = ' '.join([str(elem) for elem in convertedArray]) #converts the array to a string

    return convertedString
