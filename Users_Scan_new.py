# -*- coding: utf-8 -*-
import sys
import csv
import os

global currentDir

def checkFile(today):
    result = 1
    currentDir = os.getcwd()
    target = currentDir + "\\" + today + "\\"
    print("Checking files under : " + target)

    if (os.path.isfile(target + today + "_callrecords.csv") > 0):
        print(target + today + "_callrecords.csv checked.")
    else:
        print(target + today + "_callrecords.csv not found!")
        result = 0
        
    if (os.path.isfile(target + today + "_registered.csv") > 0):
        print(target + today + "_registered.csv checked.")
    else:
        print(target + today + "_registered.csv not found!")
        result = 0

    if (os.path.isfile(target + today + "_login.csv") > 0):
        print(target + today + "_login.csv checked.")
    else:
        print(target + today + "_login.csv not found!")
        result = 0
    return result

def checkPhone(phoneNumber, sourceFile):
    result = 0
    if os.path.isfile(sourceFile):
        fp = open(sourceFile,'r',encoding='utf-8')
        for line in fp.readlines():
            #print(">>>Comparing: " +  phoneNumber + " vs " + line)
            if (phoneNumber.strip() == line.strip()):
                result = 1
        fp.close()
    else:
        print("Can not read from file: " + sourceFile)
    return result

def scanPhone(smsFile, sourceFile):
    missingList = []
    convertedList = []
    print("Start to scan ......" + smsFile)
    if os.path.isfile(smsFile):
        fp = open(smsFile, 'r',encoding='utf-8')
        for line in fp.readlines():
            if (len(line) > 1):
                #smsPhone = line.split()[0]
                smsPhone = line.strip()
            else:
                continue
            #print("checking for phone number: " + smsPhone)
            isContained = checkPhone(smsPhone, sourceFile)
            if (isContained == 0):
                #print(smsPhone + " is missed!")
                missingList.append(smsPhone)
            else:
                print(smsPhone + " is converted!")
                convertedList.append(smsPhone)
        fp.close()
    else:
        print("Can not read from sms phone list file!")
    return len(missingList),len(convertedList)

if __name__ == "__main__":
    currentDir = os.getcwd()

    #for arg in sys.argv:
    #    print(arg)
    #print(len(sys.argv))
    if (len(sys.argv) < 2):
        print("Please input date to be calculated")
        print("Example: #>python Users_Scan_new.py 20150907")
        exit
    else:        
        today = sys.argv[1]
        ready = checkFile(today)
        if (ready == 1):
            #To check all registered users
            smsFile = currentDir + "\\" + today + "\\" + today + '_callrecords.csv'
            #sourceFile = currentDir + "\\" + today + "\\" + today + '_allusers.csv'
            #missed,converted = scanPhone(smsFile, sourceFile)
            #print("Total missed : " + str(missed))
            #print("Total registered users : " + str(converted))
            sourceFile = currentDir + "\\" + today + "\\" + today + '_registered.csv'
            missed,converted = scanPhone(smsFile, sourceFile)
            print("Today missed : " + str(missed))
            print("Today registered users : " + str(converted))
            reportFile = currentDir + "\\" + today + "\\" + today + '_login.csv'
            noreport,withreport = scanPhone(smsFile, reportFile)
            #print("Total users login : " + str(noreport))
            print("Total users login : " + str(withreport))
