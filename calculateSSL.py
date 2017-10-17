# -*- coding: utf-8 -*-
# To select stock by pressure and support within specified time range.
# 获取制定时段内的压力和支撑位置

import os
#import tushare as ts

def getLast2HighPoints(dataLines):
    #To get the Stock pressure and support point, each for 2
    #Two high points, one is latest, at the same time it's pressure line
    #And connect the two high points, get the pressure line p(t) = kt + b
    pressureList = []
    pressureDict = {}
    
    #dateIndex = 0
    highIndex = 2

    if (len(dataLines) > 41):
        titleLine = dataLines[0].split(',')
        highIndex = titleLine.index('high')
        #dateIndex = titleLine.index('date')
        
        for line in range(6,len(dataLines)-1):
            lineList = dataLines[line].split(',')
            thisHigh = float(lineList[highIndex])
            #thisDate = lineList[dateIndex]
            
            isHighPoint = True
            for i in range(1,6):
                lastLine = dataLines[line-i].split(',')
                lastHigh = float(lastLine[highIndex])
                if (thisHigh <= lastHigh):
                    isHighPoint = False
                preLine = dataLines[line+i].split(',')
                preHigh = float(preLine[highIndex])
                if (thisHigh <= preHigh):
                    isHighPoint = False
            if (isHighPoint):
                pressureList.append(thisHigh)
                #pressureDict[thisDate] = thisHigh
                pressureDict[line + 1] = thisHigh
                line += 6
            if (len(pressureList) >= 2):
                break
                
    return pressureDict
    #return pressureList

def getLast2LowPoints(dataLines):
    #To get the Stock pressure and support point, each for 2
    #Two low points, one is latest, at the same time it's support line
    #And connect the two low points, get the support line s(t) = kt + b
    supportList = []
    supportDict = {}

    lowIndex = 4
    #dateIndex = 0

    if (len(dataLines) > 41):
        titleLine = dataLines[0].split(',')
        lowIndex = titleLine.index('low')
        #dateIndex = titleLine.index('date')
        
        for line in range(6,len(dataLines)-1):
            lineList = dataLines[line].split(',')
            thisLow = float(lineList[lowIndex])
            #thisDate = lineList[dateIndex]
            
            isLowPoint = True
            for i in range(1,6):
                lastLine = dataLines[line-i].split(',')
                lastLow = float(lastLine[lowIndex])
                if (thisLow >= lastLow):
                    isLowPoint = False
                preLine = dataLines[line+i].split(',')
                preLow = float(preLine[lowIndex])
                if (thisLow >= preLow):
                    isLowPoint = False
            if (isLowPoint):
                supportList.append(thisLow)
                #supportDict[thisDate] = thisLow
                supportDict[line + 1] = thisLow
                line += 6
            if (len(supportList) >= 2):
                break
                
    #return supportList
    return supportDict

def getLineTrend(pointsDict):
    #计算压力或支撑线的斜率k
    k = 0.0    
    if (len(pointsDict) == 2):
        k = round((pointsDict.values()[1] - pointsDict.values()[0])/(pointsDict.keys()[0]-pointsDict.keys()[1]),4)
    
    #计算线性的压力或支撑点位
    linePressure = 0
    if len(pointsDict) > 1:
        linePressure = pointsDict.values()[1]
    if (k != 0):
        linePressure = k * pointsDict.keys()[0] + pointsDict.values()[0]
    return linePressure

def getTrendArea(close,pointPressure,linearPressure,pointSupport,linearSupport):
    #5=极强；4=较强；3=平衡；2=较弱；1=极弱
    #根据当前价格，判断所在压力和支撑的区间
    sslList = [close, pointPressure,linearPressure,pointSupport,linearSupport]
    sslList.sort()
    return sslList.index(close) + 1

def getTrendSymbol(trendValue):
    symbolDict = {1:"---",2:"--",3:"==",4:"++",5:"+++"}
    symbol = "=="
    if (symbolDict.has_key(trendValue)):
        symbol = symbolDict.get(trendValue)
    return symbol

def calculateSSL(csvDir, sslDir):
    csvFileSuffix = ".csv"
    csvList = os.listdir(csvDir)
    #print(csvList)
    
    #analyze all csv files in the loop one by one
    print("start to analyzing Pressure/Support for all ...")
    for csvFile in csvList:
        if csvFile[-4:] == '.csv':
            csvName = csvFile[0:-4]
            targetName = csvName + "_SSL" + csvFileSuffix
            source = os.path.join(csvDir, csvFile)
            target = os.path.join(sslDir, targetName)
            
            fSource = open(source, 'r')
            dataLines = fSource.readlines()
            if len(dataLines) < 2:
                continue
            lastDate = str(dataLines[1].split(',')[0])
            lastPrice = float(dataLines[1].split(',')[3])
            
            #获取压力和支撑点集合，各取最近的两个点
            pressurePoints = getLast2HighPoints(dataLines)
            supportPoints = getLast2LowPoints(dataLines)
            linearPressure = round(getLineTrend(pressurePoints),2)
            linearSupport = round(getLineTrend(supportPoints),2)
            #print lastPrice,pressurePoints.values()[1],linearPressure,supportPoints.values()[1],linearSupport
            trend = getTrendArea(lastPrice,pressurePoints.values()[1],linearPressure,supportPoints.values()[1],linearSupport)
            #print trend
            symbol = getTrendSymbol(trend)
            
            if (os.path.isfile(target) > 0):
                fTarget = open(target, 'r')
                targetLines = fTarget.readlines()
                targetDate = str(targetLines[-1].split(',')[0])
                
                if (lastDate == targetDate):
                    print("%s already updated!" % (csvName))
                    fTarget.close()
                    fSource.close()
                    continue
                fTarget = open(target, 'a')
                fTarget.write(str(lastDate) + "," + str(lastPrice) + "," + str(pressurePoints.values()[1]) + "," + str(linearPressure) + "," + str(supportPoints.values()[1]) + "," + str(linearSupport) + "," + str(trend) + "," + symbol + "\n")
            else:
                fTarget = open(target, 'w')
                fTarget.write("date,price,point-pressure,linear-pressure,point-support,linear-support" + "\n")
                fTarget.write(str(lastDate) + "," + str(lastPrice) + "," + str(pressurePoints.values()[1]) + "," + str(linearPressure) + "," + str(supportPoints.values()[1]) + "," + str(linearSupport) + "," + str(trend) + "," + symbol + "\n")
            #close files
            if ( not fSource.closed):
                fSource.close()
            if ( not fTarget.closed):
                fTarget.close()
            
            if (os.path.isfile(source) > 0):
                #read source file
                fSource = open(source, 'r')
                fTarget = open(target, 'r')
                dataLines = fSource.readlines()
                
                lastDate = str(dataLines[1].split(',')[0])
                lastPrice = float(dataLines[1].split(',')[3])
                targetLines = fTarget.readlines()
                targetDate = str(targetLines[-1].split(',')[0])
                if (lastDate == targetDate):
                    print("already updated!")
                    fTarget.close()
                    fSource.close()
                    continue                
        else:
            continue
    print("SSL analyzing completed!")
    #End of for loop
    
if __name__ == "__main__":
    pathSep = "/"
    
    currentDir = os.getcwd()
    csvDir = currentDir + "/csv"
    sslDir = currentDir + "/ssl"
    #get Date here, and to load latest data automaticaly.
    
    calculateSSL(csvDir, sslDir)