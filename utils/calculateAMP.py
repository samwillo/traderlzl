# -*- coding: utf-8 -*-
# To select stock by amplitude within specified time range.
# 获取制定时段内的平均振幅

import os
import time
#import tushare as ts

def getAvgAmplitude(dataLines, days):
    #To get the Stock Amplitude for specified past days range. for example, 5, 10, 20, 40 days AVG amplitude
    ampList = []
    avgAmp = 0.0
    
    highIndex = 2
    closeIndex = 3
    lowIndex = 4

    if (len(dataLines) > 42):
        titleLine = dataLines[0].split(',')
        highIndex = titleLine.index('high')
        closeIndex = titleLine.index('close')
        lowIndex = titleLine.index('low')
        
        for line in range(1,days+1):
            lineList = dataLines[line].split(',')
            thisHigh = float(lineList[highIndex])
            thisLow = float(lineList[lowIndex])
            lastLine = dataLines[line+1].split(',')
            lastClose = float(lastLine[closeIndex])
            
            ampList.append((thisHigh - thisLow)/lastClose)
        #End of for cycle
        avgAmp = getAvgOfList(ampList)
                
    return avgAmp

def getAvgOfList(myList):
    tmp = 0.0
    for i in range(0,len(myList)):
        tmp += myList[i]
    return round(float(tmp/len(myList)),4)

def calculateAMP(csvDir,ampDir):
    csvFileSuffix = ".csv"
    csvList = os.listdir(csvDir)
    #analyze all csv files in the loop one by one
    print("start to analyzing amplitude for all ...")
    for csvFile in csvList:
        if csvFile[-4:] == '.csv':
            csvName = csvFile[0:-4]
            targetName = csvName + "_AMP" + csvFileSuffix
            source = os.path.join(csvDir, csvFile)
            target = os.path.join(ampDir, targetName)
            
            fSource = open(source, 'r')
            dataLines = fSource.readlines();
            if len(dataLines) < 2:
                continue
            
            lastDate = str(dataLines[1].split(',')[0])
            
            amp = getAvgAmplitude(dataLines,1)
            amp5 = getAvgAmplitude(dataLines, 5)
            amp10 = getAvgAmplitude(dataLines, 10)
            amp20 = getAvgAmplitude(dataLines, 20)
            amp40 = getAvgAmplitude(dataLines, 40)
            
            if (os.path.isfile(target) > 0):
                #read source file
                fTarget = open(target, 'r')
                targetLines = fTarget.readlines()
                targetDate = str(targetLines[-1].split(',')[0])
                #print("csv date " + str(lastDate))
                #print("amp date " + str(targetDate))
                if (lastDate == targetDate):
                    print("already updated!")
                    fTarget.close()
                    fSource.close()
                    continue
                
                fTarget = open(target, 'a')
                fTarget.write(str(lastDate) + "," + str(amp) + "," + str(amp5) + "," + str(amp10) + "," + str(amp20) + "," + str(amp40) + "\n")
            else:
                fTarget = open(target, 'w')
                fTarget.write("date,amp,amp5,amp10,amp20,amp40" + "\n")
                fTarget.write(str(lastDate) + "," + str(amp) + "," + str(amp5) + "," + str(amp10) + "," + str(amp20) + "," + str(amp40) + "\n")
                
            #close files
            if ( not fSource.closed):
                fSource.close()
            if ( not fTarget.closed):
                fTarget.close()
                #close files
            if (amp5 > 0.03):
                print(csvName + ":")
                print(" 5 days average amplitude: " + str(amp5))
                print(" 10 days average amplitude: " + str(amp10))
                print(" 20 days average amplitude: " + str(amp20))
                print(" 40 days average amplitude: " + str(amp40))
        else:
            continue
    print("Amplitude analyzing completed!")
    #End of for loop

if __name__ == "__main__":
    pathSep = "／"
    #csvFileSuffix = ".csv"
    #currentDir = os.getcwd()
    currentDir = "/Users/liuzl/workspace/python/traderlzl8/data"
    csvDir = currentDir + "/csv"
    ampDir = currentDir + "/amp"
    today = time.strftime("%Y-%m-%d", time.localtime())
    #get Date here, and to load latest data automaticaly.
    #csvList = os.listdir(csvDir)
    #print(csvList)
    
    calculateAMP(csvDir, ampDir)
    

