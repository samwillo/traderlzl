# -*- coding: utf-8 -*-

import os
import sys

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

def getCHA(dataDir, stockCode):
    dataFile = stockCode + "_CHA.csv"
    source = os.path.join(dataDir, dataFile)
    if (os.path.isfile(source) > 0):
        #read source file and convert
        fSource = open(source, 'r')
        dataLines = fSource.readlines();
        print('================================================================')
        print(u'股票属性分析：' + str(stockCode))
        for line in range(0,len(dataLines)):
            print(dataLines[line][:-1])
    else:
        print("stock data not included!")
    
def getAMP(dataDir, stockCode):
    dataFile = stockCode + "_AMP.csv"
    source = os.path.join(dataDir, dataFile)
    if (os.path.isfile(source) > 0):
        #read source file and convert
        fSource = open(source, 'r')
        dataLines = fSource.readlines();
        print('================================================================')
        print(u'近期振幅统计：' + str(stockCode)) 
        print(dataLines[0][:-2])
        print(dataLines[-1][:-2])
    else:
        print("stock data not included!")
            
def getSSL(dataDir, stockCode):
    dataFile = stockCode + "_SSL.csv"
    source = os.path.join(dataDir, dataFile)
    if (os.path.isfile(source) > 0):
        #read source file and convert
        fSource = open(source, 'r')
        dataLines = fSource.readlines();
        print('================================================================')
        print(u'压力支撑分析：' + str(stockCode))
        print(dataLines[0][:-2])
        if len(dataLines) > 2:
            print(dataLines[-2][:-2])
        print(dataLines[-1][:-2])
    else:
        print("stock data not included!")

def getTOR(dataDir, stockCode):
    dataFile = stockCode + "_TOR.csv"
    source = os.path.join(dataDir, dataFile)
    if (os.path.isfile(source) > 0):
        #read source file and convert
        fSource = open(source, 'r')
        dataLines = fSource.readlines();
        print('================================================================')
        print(u'换手率统计：' + str(stockCode))
        for line in range(0,3):
            print(dataLines[line][:-2])
    else:
        print("stock data not included!")

def analyze(currentDir,code):
    
    #csvDir = currentDir + "/csv/"
    ampDir = currentDir + "/amp"
    sslDir = currentDir + "/ssl"
    chaDir = currentDir + "/cha"
    torDir = currentDir + "/tor"
    if len(code) == 6:
        print('================================================================')
        print("========       * Code: %s,  Name: %s *       ========" % (code, getStockName(currentDir,code)))
        getCHA(chaDir, str(code))
        getTOR(torDir, str(code))
        getAMP(ampDir, str(code))
        getSSL(sslDir, str(code))
        print('================================================================')

if __name__ == "__main__":
    
    currentDir = os.getcwd()
    print("[INFO] Current working directory is: %s " % (currentDir))
    csvDir = currentDir + "/csv/"
    ampDir = currentDir + "/amp"
    sslDir = currentDir + "/ssl"
    chaDir = currentDir + "/cha"
    torDir = currentDir + "/tor"
    
    if (len(sys.argv) < 1):
        print("Please input stock code to be analyzed.....")
        print("Example: #>python 600001")
        exit
    else:        
        stockCode = sys.argv[1]
        analyze(currentDir, stockCode)
    
    
    

