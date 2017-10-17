# -*- coding: utf-8 -*-

import os
import time
#import tushare as ts
import downloadData
import calculateTOR
import calculateAMP
import calculateCHA
import calculateSSL
import stockAnalyze
import stockSelect

def get_download_tag():
    tag = open("latest",'r')
    return tag.readline().strip()

def update_download_tag(update_date):
    tag = open("latest",'w')
    tag.write(update_date)
    
def calculate_TOR():
    calculateTOR.calculateTOR(csvDir, torDir)
    
def calculate_AMP():
    calculateAMP.calculateAMP(csvDir, ampDir)
    
def calculate_CHA():
    calculateCHA.calculateCHA(csvDir, chaDir)
    
def calculate_SSL():
    calculateSSL.calculateSSL(csvDir, sslDir)
    
def calculate_ALL():
    calculateTOR.calculateTOR(csvDir, torDir)
    calculateAMP.calculateAMP(csvDir, ampDir)
    calculateCHA.calculateCHA(csvDir, chaDir)
    calculateSSL.calculateSSL(csvDir, sslDir)
    
def stock_Analyze(currentDir, code):
    stockAnalyze.analyze(currentDir, code)
    
def stock_Select(currentDir):
    stockSelect.selectStock(currentDir)
    
if __name__ == "__main__":
    
    #get local date first
    startDate = "2017-01-01"
    today = time.strftime("%Y-%m-%d", time.localtime())
    print("[INFO] Downloading stock data on: " + today)
    
    currentDir = os.getcwd()
    print("[INFO] Current working directory is: %s " % (currentDir))
    csvDir = currentDir + "/csv/"
    torDir = currentDir + "/tor/"
    ampDir = currentDir + "/amp/"
    chaDir = currentDir + "/cha/"
    sslDir = currentDir + "/ssl/"
    #csvFileSuffix = ".csv"
    
    fCodes = open(os.path.join(currentDir, "stock_codes.csv"),'r')
    codesList = fCodes.readlines()
    #Start to download daily K data for all stock in stock_codes.csv 
    if (len(codesList) > 0):
        if get_download_tag() == today:
            print("[INFO] Already latest.")
        else:
            total = len(codesList)
            completed = 0
            for code in codesList:
                code = code.strip()
                #print("stock code = %s, %s" % (code, type(code)))
                downloadData.getBasicData(code, csvDir, startDate, today, 'D')
                #data = ts.get_hist_data(code=code,start=startDate,end=today,ktype='D',retry_count=3,pause=1)
                #print("Got data type: %s" % (type(data)))
                completed += 1
                print("[INFO] Downloaded data for : " + code)
                print("[INFO] Downloading process : %s of %s" % (completed, total))
            update_download_tag(today)
    else:
        print("[ERROR] Check codes.csv please! no codes found.")
        
    #To run the cmd based tool to do analyzing
    while True:
        print("[PROMPT] Input your choice to do analysis:")
        print("    1 -> Calculate TOR; 2 -> Calculate AMP; 3 -> Calculate CHA; 4 -> Calculate SSL;")
        print("    5 -> Calculate All; 6 -> Stock Analyzing; 7 -> Stock Selecting; 0 -> Exit")
        
        user_choice = int(raw_input("    Please enter the number: "))
        print "    You choosed %s......" % (user_choice)
        
        choices = {
            1: calculate_TOR,
            2: calculate_AMP,
            3: calculate_CHA,
            4: calculate_SSL,
            5: calculate_ALL,
        }
        
        if user_choice > 7 or user_choice ==0:
            break
        if user_choice == 6:
            stockCode = str(raw_input("    Please enter one stock code: "))
            stock_Analyze(currentDir, stockCode.strip())
        elif user_choice ==7:
            stock_Select(currentDir)
        else:
            choosed_func = choices[user_choice]
            choosed_func()
        
            
    
    
    