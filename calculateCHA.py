# -*- coding: utf-8 -*-
# To select stock by amplitude within specified time range.
# 获取股票的统计属性

#import sys
#import csv
import os
#import tushare as ts

#Get stock name by searching the stock concept_classified.csv file
def getStockName(currentDir, code):
    name = ""
    classifier = os.path.join(currentDir + "/classifiers", "concept_classified.csv")
    f_classifier = open(classifier, 'r')
    lines = f_classifier.readlines()
    
    for info in lines:
        info_list = info.split(',')
        if info_list[0] == code:
            name = info_list[1]
    return name

def getHigLowRange(dataLines):
    #To get the highest and lowest price for the specified period, which included in the dataList
    highPoint = 0.0
    lowPoint = 1000.0
    gainDays = 0
    fallDays = 0
    flatDays = 0
    highIndex = 2
    lowIndex = 4
    pChangeIndex = 7
    
    if (len(dataLines) > 1):
        titleLine = dataLines[0].split(',')
        highIndex = titleLine.index('high')
        lowIndex = titleLine.index('low')
        pChangeIndex = titleLine.index('p_change')
        
        for line in range(1,len(dataLines)-1):
            lineList = dataLines[line].split(',')
            thisHigh = float(lineList[highIndex])
            thisLow = float(lineList[lowIndex])
            thispChange = float(lineList[pChangeIndex])
            
            if (thisHigh > highPoint):
                highPoint = thisHigh
  
            if (thisLow < lowPoint):
                lowPoint = thisLow
            
            if (thispChange > 0):
                gainDays += 1
            elif (thispChange < 0):
                fallDays += 1
            elif (thispChange == 0):
                flatDays += 1
            else:
                continue
            
        #End of for cycle        
    return highPoint, lowPoint, gainDays, fallDays, flatDays

def getTradingDaysStat(dataLines):
    #To calculate the probabilities of continous up or fall.
    #List to save continous up days
    contUpList = []
    #List to save continous fall days
    contFallList = []
    
    pChangeIndex = 7
    
    if (len(dataLines) > 1):
        titleLine = dataLines[0].split(',')
        pChangeIndex = titleLine.index('p_change')
        
        tmpContUp = 0
        tmpContFall = 0
        isContUp = 1
        for line in range(1,len(dataLines)-1):
            lineList = dataLines[line].split(',')
            thispChange = float(lineList[pChangeIndex])
            if (thispChange > 0):
                if (isContUp == 1):
                    tmpContUp += 1
                else:
                    isContUp = 1
                    contFallList.append(tmpContFall)
                    tmpContFall = 0
                    tmpContUp += 1
            elif (thispChange < 0):
                if (isContUp == 0):
                    tmpContFall += 1
                else:
                    isContUp = 0
                    contUpList.append(tmpContUp)
                    tmpContUp = 0
                    tmpContFall += 1
        #end for loop
            
    maxUpDays = max(contUpList)
    timesOfMaxUp = contUpList.count(maxUpDays)
    maxFallDays = max(contFallList)
    timesOfMaxFall = contFallList.count(maxFallDays)
    
    probUpDict = {}
    probFallDict = {}
    
    for days in range(1,maxUpDays+1):
        probUpDict[days] = round(float(contUpList.count(days))/float(len(contUpList)),2)
    for days in range(1,maxFallDays+1):
        probFallDict[days] = round(float(contFallList.count(days))/float(len(contFallList)),2)
    
    #print(probUpDict, probFallDict)
    return maxUpDays, timesOfMaxUp, maxFallDays, timesOfMaxFall, probUpDict, probFallDict

def calculateCHA(csvDir, chaDir):
    csvFileSuffix = ".csv"
    csvList = os.listdir(csvDir)
    #print(csvList)
    
    #analyze all csv files in the loop one by one
    print("start to analyzing charactor for all ...")
    for csvFile in csvList:
        if csvFile[-4:] == '.csv':
            csvName = csvFile[0:-4]
            targetName = csvName + "_CHA" + csvFileSuffix
            source = os.path.join(csvDir, csvFile)
            target = os.path.join(chaDir, targetName)
            
            if (os.path.isfile(source) > 0):
                #read source file
                fSource = open(source, 'r')
                fTarget = open(target, 'w')
                dataLines = fSource.readlines();
                if len(dataLines) < 2:
                    continue
                lastDate = str(dataLines[1].split(',')[0])
                #Get charactor
                #period = len(dataLines) - 1
                highPoint, lowPoint, gainDays, fallDays, flatDays  = getHigLowRange(dataLines)
                maxUpDays, timesOfMaxUp, maxFallDays, timesOfMaxFall, probUpDict, probFallDict = getTradingDaysStat(dataLines)
                
                fTarget.write("Code : " + csvName + "\n")
                fTarget.write("Last trading date : " + lastDate + "\n")
                fTarget.write("Analyzing from : " + "2017-01-01" + "\n")
                fTarget.write("HIGH point, LOW point : " + str(highPoint) + ", " + str(lowPoint) + "\n")
                fTarget.write("GAIN days total : " + str(gainDays) + "\n")
                fTarget.write("FALL days total : " + str(fallDays) + "\n")
                fTarget.write("FLAT days total : " + str(flatDays) + "\n")
                fTarget.write("Continous UP days MAX : " + str(maxUpDays) + "\n")
                fTarget.write("Times of MAX UP days  : " + str(timesOfMaxUp) + "\n")
                fTarget.write("Continous FALL days MAX : " + str(maxFallDays) + "\n")
                fTarget.write("Times of MAX FALL days  : " + str(timesOfMaxFall) + "\n")
                fTarget.write("Continous UP days Probability : " + str(probUpDict) + "\n")
                fTarget.write("Continous FALL days Probability : " + str(probFallDict) + "\n")
                #close files
                fSource.close()
                fTarget.close()                        
            print("Calculate CHA for %s done!" % (csvFile))
        else:
            continue
    #End of for loop
    
if __name__ == "__main__":
    pathSep = "/"
    
    currentDir = os.getcwd()
    csvDir = currentDir + "/csv"
    chaDir = currentDir + "/cha"
    #get Date here, and to load latest data automaticaly.
    calculateCHA(csvDir, chaDir)
    
    
    