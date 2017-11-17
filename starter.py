# -*- coding: utf-8 -*-

import os
import time
#import tushare as ts
from utils import downloadData
#from stat import calculateTOR
from utils import calculateTOR
from utils import calculateAMP
from utils import calculateCHA
from utils import calculateSSL
from utils import calculateCHG
from analyze import stockAnalyze
from analyze import stockSelect
from analyze import sslVerify

def get_download_tag():
    tag = open("latest",'r')
    return tag.readline().strip()
    tag.close()

def update_download_tag(update_date):
    tag = open("latest",'w')
    tag.write(update_date)
    tag.close()
    
def calculate_TOR():
    calculateTOR.calculateTOR(csvDir, torDir)
    
def calculate_AMP():
    calculateAMP.calculateAMP(csvDir, ampDir)
    
def calculate_CHA():
    calculateCHA.calculateCHA(csvDir, chaDir)
    
def calculate_CHG():
    calculateCHG.calculateCHG(csvDir, chgDir)
    
def calculate_SSL():
    calculateSSL.calculateSSL(csvDir, sslDir)
    
def calculate_ALL():
    calculateTOR.calculateTOR(csvDir, torDir)
    calculateAMP.calculateAMP(csvDir, ampDir)
    calculateCHA.calculateCHA(csvDir, chaDir)
    calculateSSL.calculateSSL(csvDir, sslDir)
    calculateCHG.calculateCHG(csvDir, chgDir)
    
def stock_Analyze(currentDir, code):
    stockAnalyze.analyze(currentDir, code)
    
def stock_Select(currentDir):
    stockSelect.selectStock(currentDir)
    
def run_SSLVerify(sslDir, code):
    sslVerify.sslVerify(sslDir, code)
    
if __name__ == "__main__":
    
    #get local date first
    startDate = "2017-01-01"
    today = time.strftime("%Y-%m-%d", time.localtime())
    print("[INFO] Downloading stock data on: " + today)
    
    currentDir = os.getcwd()
    print("[INFO] Current working directory is: %s " % (currentDir))
    dataDir = currentDir + "/data/"
    confDir = currentDir + "/conf/"
    indexDir = dataDir + "/indexData/"
    csvDir = dataDir + "/csv/"
    torDir = dataDir + "/tor/"
    ampDir = dataDir + "/amp/"
    chaDir = dataDir + "/cha/"
    chgDir = dataDir + "/chg/"
    sslDir = dataDir + "/ssl/"
    #csvFileSuffix = ".csv"
    
    fCodes = open(os.path.join(confDir, "stock_codes.csv"),'r')
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
                
            downloadData.getIndexData(indexDir, today)
            update_download_tag(today)
    else:
        print("[ERROR] Check codes.csv please! no codes found.")
        
    #To run the cmd based tool to do analyzing
    while True:
        print("[PROMPT] Input your choice to do analysis:")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("|   1 -> Calculate TOR; 2 -> Calculate AMP; 3 -> Calculate CHA;                    |")
        print("|   4 -> Calculate SSL; 5 -> Calculate CHG; 6 -> Calculate All;                    |")
        print("|   7 -> Stock Selecting; 8 -> Stock Analyzing; 9 -> Run Verify Test;              |")
        print("|   0 -> Exit                                                                      |")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        
        user_choice = int(raw_input("    Please enter the number: "))
        print "    You choosed %s......" % (user_choice)
        
        choices = {
            1: calculate_TOR,
            2: calculate_AMP,
            3: calculate_CHA,
            4: calculate_SSL,
            5: calculate_CHG,
            6: calculate_ALL,
        }
        if user_choice ==0:
            break
        elif user_choice > 9:
            continue
        elif user_choice == 9:
            stockCode = str(raw_input("    Please enter one stock code: "))
            run_SSLVerify(sslDir, stockCode)
        elif user_choice == 8:
            stockCode = str(raw_input("    Please enter one stock code: "))
            stock_Analyze(dataDir, stockCode.strip())
        elif user_choice ==7:
            stock_Select(dataDir)
        else:
            choosed_func = choices[user_choice]
            choosed_func()
        