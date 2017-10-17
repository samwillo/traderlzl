# -*- coding: utf-8 -*-
# To select stock by amplitude within specified time range.
# 计算换手率

#import sys
#import csv
import os
#import tushare as ts

def convertTOR(source, target):
    result = 1
    #semi = ','
    dateIndex = 0
    pChangeIndex = 7
    turnoverIndex = 14
    
    if (os.path.isfile(source) > 0):
        #read source file and convert
        fSource = open(source, 'r')
        fTarget = open(target, 'w')
        dataLines = fSource.readlines();

        if (len(dataLines) > 1):
            titleLine = dataLines[0].split(',')
            dateIndex = titleLine.index('date')
            pChangeIndex = titleLine.index('p_change')
            turnoverIndex = titleLine.index('turnover\n')
            targetTitleLine = "date,p_change,TOR,TOR_3,TOR_5,TOR_10,TOR_15\n"
            fTarget.write(targetTitleLine)
            
            for line in range(1,len(dataLines)-16):
            #for line in range(1,100):
                #calculate TOR and save to target file
                lineList = dataLines[line].split(',')
                dateTarget = lineList[dateIndex]
                pChangeTarget = lineList[pChangeIndex]
                turnoverTarget = lineList[turnoverIndex][:-1]
                
                TOR_avg_3 = 0
                for i in range(0,2):
                    TOR_avg_3 += round(float(dataLines[line + i].split(',')[turnoverIndex][:-1]),3)
                TOR_avg_3 = round(TOR_avg_3/3,3)
                
                TOR_avg_5 = 0
                for i in range(0,4):
                    TOR_avg_5 += round(float(dataLines[line + i].split(',')[turnoverIndex][:-1]),3)
                TOR_avg_5 = round(TOR_avg_5/5,3)
                
                TOR_avg_10 = 0
                for i in range(0,9):
                    TOR_avg_10 += round(float(dataLines[line + i].split(',')[turnoverIndex][:-1]),3)
                TOR_avg_10 = round(TOR_avg_10/10,3)
                
                TOR_avg_15 = 0
                for i in range(0,14):
                    TOR_avg_15 += round(float(dataLines[line + i].split(',')[turnoverIndex][:-1]),3)
                TOR_avg_15 = round(TOR_avg_15/15,3)              
                
                targetLine = str(dateTarget) + "," + str(pChangeTarget) + "," + str(turnoverTarget) + "," + str(TOR_avg_3) + "," + str(TOR_avg_5) + "," + str(TOR_avg_10) + "," + str(TOR_avg_15) + "\n" 
                fTarget.write(targetLine)
            #end of for cycle
            
        fSource.close()
        fTarget.close()
        result = 1
    else:
        print("File " + source + " not exist!")
        result = 0
        
    return result

def calculateTOR(csvDir, torDir):
    csvFileSuffix = ".csv"
    csvList = os.listdir(csvDir)
    #print(csvList)
    
    #analyze all csv files in the loop one by one
    print("start to analyze files...")
    for csvFile in csvList:
        if csvFile[-4:] == '.csv':
            csvName = csvFile[0:-4]
            targetName = csvName + "_TOR" + csvFileSuffix
            if (convertTOR(os.path.join(csvDir, csvFile), os.path.join(torDir, targetName)) > 0):
                print("File: " + csvFile + " was converted!")
            else:
                print("Failed to convert CSV file: " + csvFile)
        else:
            continue

if __name__ == "__main__":
    pathSep = "/"
    #csvFileSuffix = ".csv"
    currentDir = os.getcwd()
    csvDir = currentDir + "/csv"
    torDir = currentDir + "/tor"
    #get Date here, and to load latest data automaticaly.
    calculateTOR(csvDir, torDir)
        
