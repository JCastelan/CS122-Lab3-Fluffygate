#!/usr/bin/env python3

"""
Script usage:

    python pAutomation.py <username> <passwdPCAPFile> <IVPCAPFile> <keyPCAPFile> <msgPCAPFile>
"""

import os
import sys
import pcap
import unzip
import decrypt
import keyParser
import NSARequests as nsa
import multiprocessing as mp

#
PCAP_DIRECTORY = "../"

PASS_OUTPUTFILE = "../passOutput"

#Constant values
PASWWD_FILE = "passwd"
IV_FILE = "iv"
KEY_FILE = "key.zip"
MESSAGE_FILE = "cipherMessage"
PASSWORD_PLAIN = "password.plain"
KEY_PLAIN = "key"
KEY_PARSED = "key.parsed"

#Const values
NSA_HOST = '128.114.59.42'
NSA_PORT = 2001
LOCAL_HOST = '128.114.59.29 '
LOCAL_PORT = 52696 

MAX_USERS = 10

def createDirectories(username):

    dataFolder = "../" + username + "Data/"
    if not os.path.exists(dataFolder): 
        os.makedirs(dataFolder)

    outFolder = "../" + username + "Output/"
    if not os.path.exists(outFolder): 
        os.makedirs(outFolder)

    dmsgFolderOne = outFolder + "decriptedMessageOne/"
    if not os.path.exists(dmsgFolderOne): 
        os.makedirs(dmsgFolderOne)

    dmsgFolderTwo = outFolder + "decriptedMessageTwo/"
    if not os.path.exists(dmsgFolderTwo): 
        os.makedirs(dmsgFolderTwo)

    dmsgFolderThree = outFolder + "decriptedMessageThree/"
    if not os.path.exists(dmsgFolderThree): 
        os.makedirs(dmsgFolderThree)

    return dataFolder, outFolder, dmsgFolderOne, dmsgFolderTwo, dmsgFolderThree

def forAllCreateDirectories(usernames):

    dataFolders, outFolders, dmsgFolderOne, dmsgFolderTwo, dmsgFolderThree = [],[],[],[],[]

    for user in usernames:
        #DATA_FOLDER, OUT_FOLDER, DMSG_FOLDER = createDirectories(username)
        dFolder, oFolder, mFolder1, mFolder2, mFolder3 = createDirectories(user)
        dataFolders.append(dFolder)
        outFolders.append(oFolder) 
        dmsgFolderOne.append(mFolder1)
        dmsgFolderTwo.append(mFolder2)
        dmsgFolderThree.append(mFolder3)


    return dataFolders, outFolders, dmsgFolderOne, dmsgFolderTwo, dmsgFolderThree

def requests(passwd_files, outputFile):
    """Prints all responses to arbitrary outputFile"""

    cPasswds = []

    for pfile in passwd_files:
        #Obtain encrypted password
        cryptFile = open(pfile, "r")
        cryptedPass=cryptFile.readline().strip()+' '

        cPasswds.append(cryptedPass)

    #!!!Later on change port to be random and check if its used
    #Send request in a child process
    userProcess = mp.Process(target=nsa.NSA_user, args=((LOCAL_HOST, LOCAL_PORT, cPasswds)) )
    userProcess.start()

    #Listener
    nsa.NSA_listener('', LOCAL_PORT, outputFile, len(cPasswds) )

    #Join child process
    userProcess.join() 

def automation(usernames, passwdPCAPFiles, ivPCAPFiles, keyPCAPFiles, msgOnePCAPFiles, msgTwoPCAPFiles, msgthreePCAPFiles):

    numberOfUsers = len(usernames)

    if numberOfUsers > MAX_USERS:
        print "Maximum number of users exceded."
        return

    #------------------------CREATE NEW DIRECTORIES FOR ALL USERS------------------------

    DATA_FOLDERS, OUT_FOLDERS, DMSG_FOLDERS_ONE, DMSG_FOLDERS_TWO, DMSG_FOLDERS_THREE = forAllCreateDirectories(usernames)
    
    #-------------------------------Generate input pcap file paths-------------------------

    USERNAMES, PASWWD_PCAPS, IV_PCAPS, KEY_PCAPS, MESSAGE_1_PCAPS, MESSAGE_2_PCAPS, MESSAGE_3_PCAPS = [],[],[],[],[],[],[]

    for i in range(numberOfUsers):

        #User input should be the username followed by 4 PCAP files
        USERNAMES.append(usernames[i] + '_')
        PASWWD_PCAPS.append(PCAP_DIRECTORY + passwdPCAPFiles[i])
        IV_PCAPS.append(PCAP_DIRECTORY + ivPCAPFiles[i])
        KEY_PCAPS.append(PCAP_DIRECTORY + keyPCAPFiles[i])
        MESSAGE_1_PCAPS.append(PCAP_DIRECTORY + msgOnePCAPFiles[i])
        MESSAGE_2_PCAPS.append(PCAP_DIRECTORY + msgTwoPCAPFiles[i])
        MESSAGE_3_PCAPS.append(PCAP_DIRECTORY + msgthreePCAPFiles[i])


    #--------------------------Generate output data file, and extract data ----------------------------

    passwd_files, iv_files, key_files, message_one_files, message_two_files, message_three_files = [],[],[],[],[],[]

    for i in range(numberOfUsers):
        
        #Username specific file names (extract from corresponding pcap files)
        passwd_files.append(DATA_FOLDERS[i] + USERNAMES[i] + PASWWD_FILE)
        iv_files.append(DATA_FOLDERS[i] + USERNAMES[i] + IV_FILE)
        key_files.append(DATA_FOLDERS[i] + USERNAMES[i] + KEY_FILE)
        message_one_files.append(DATA_FOLDERS[i] + USERNAMES[i] + MESSAGE_FILE + '1')
        message_two_files.append(DATA_FOLDERS[i] + USERNAMES[i] + MESSAGE_FILE + '2')
        message_three_files.append(DATA_FOLDERS[i] + USERNAMES[i] + MESSAGE_FILE + '3')

        #Generate data files from PCAP files
        pcap.getPasswd( PASWWD_PCAPS[i], passwd_files[i])
        pcap.getIV( IV_PCAPS[i], iv_files[i])
        pcap.getZip( KEY_PCAPS[i], key_files[i])
        pcap.getCipherMessage( MESSAGE_1_PCAPS[i], message_one_files[i]) 
        pcap.getCipherMessage( MESSAGE_2_PCAPS[i], message_two_files[i]) 
        pcap.getCipherMessage( MESSAGE_3_PCAPS[i], message_three_files[i]) 

    #----------------------------NSA Request--------------------------------

    #requests(passwd_files, PASS_OUTPUTFILE)

    #----------------------------Write passwords to files--------------------------------
    
    passwd_plains = []
    
    #Get file contents to a list
    with open(PASS_OUTPUTFILE) as f:
        content = f.readlines()

    passwds = []

    for i in range(numberOfUsers):

        #obtain password
        p = content[i].strip()
        p = p.split(" ")[1]
        passwds.append(p)

        #create plain password file path
        passwd_plains.append(OUT_FOLDERS[i] + USERNAMES[i] + PASSWORD_PLAIN)

        #write password plain file
        pFile = open(passwd_plains[i], "w")
        pFile.write(passwds[i] + '\n')
        pFile.close()

    #--------------------------Unzip Keys----------------------------

    key_plains = []

    for i in range(numberOfUsers):
        
        #Unzip and create key file
        key_plains.append(OUT_FOLDERS[i] + USERNAMES[i] + KEY_PLAIN)
        unzip.unzipFile(key_files[i], key_plains[i], passwds[i])

    #--------------------------Parse Key----------------------------

    parsed_keys = []

    for i in range(numberOfUsers):

        parsed_keys.append(OUT_FOLDERS[i] + USERNAMES[i] + KEY_PARSED)
        keyParser.keyParsing(key_plains[i], parsed_keys[i])

    #--------------------------Decrypt---------------------------
    for i in range(numberOfUsers):

        decrypt.callDecryptShell(message_one_files[i], iv_files[i], parsed_keys[i], DMSG_FOLDERS_ONE[i])
        decrypt.callDecryptShell(message_two_files[i], iv_files[i], parsed_keys[i], DMSG_FOLDERS_TWO[i])
        decrypt.callDecryptShell(message_three_files[i], iv_files[i], parsed_keys[i], DMSG_FOLDERS_THREE[i])

def main():

    users = ["sampleUser"]
    passwdPCAPFiles = ["phase3_00003_20180304113348.pcap"] 
    keyPCAPFiles = ["phase3_00011_20180304113348.pcap"]
    ivPCAPFiles = ["phase3_00019_20180304113348.pcap"]
    msgOnePCAPFiles = ["phase3_00027_20180304113348.pcap"]
    msgTwoPCAPFiles = ["phase3_00035_20180304113348.pcap"]
    msgThreePCAPFiles = ["phase3_00043_20180304113348.pcap"]

    automation(users, passwdPCAPFiles, ivPCAPFiles, keyPCAPFiles, msgOnePCAPFiles, msgTwoPCAPFiles, msgThreePCAPFiles)
    

if __name__ == '__main__':
    main()