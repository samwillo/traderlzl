# -*- coding: utf-8 -*-

import os
import time

def selectByAMP(ampDir, threshold):
    #simple condition: if latest amp value more than specified threshold.
    stockList = []
    ampList = os.listdir(ampDir)
    
    for ampFile in ampList:
        if ampFile[-4:] == '.csv':
            source = os.path.join(ampDir, ampFile)
            fSource = open(source, 'r')
            
            dataLines = fSource.readlines();
            lastLine = dataLines[-1]
            if (float(lastLine.split(',')[1]) > 0.03):
                stockCode = ampFile[:6]
                stockList.append(stockCode)
                #print("Code :: " + str(stockCode))
                #print(dataLines[0])
                #print(lastLine)
                #print("==============================================\n")
    return stockList

def selectBySSL(sslDir):
    #simple condition: if trend value increase to higher level.
    stockBuyList = []
    stockSellList = []
    sslList = os.listdir(sslDir)
    
    for sslFile in sslList:
        if sslFile[-4:] == '.csv':
            source = os.path.join(sslDir, sslFile)
            fSource = open(source, 'r')
            
            dataLines = fSource.readlines();
            if (len(dataLines) >= 3):
                lastLine = dataLines[-1]
                last2ndLine = dataLines[-2]
                if (float(lastLine.split(',')[6]) > float(last2ndLine.split(',')[6])):
                    stockCode = sslFile[:6]
                    stockBuyList.append(stockCode)
                    #print("Code :: " + str(stockCode) + " +++")
                    #print(dataLines[0])
                    #print(last2ndLine)
                    #print(lastLine)
                    #print("==============================================\n")
                elif (float(lastLine.split(',')[6]) < float(last2ndLine.split(',')[6])):
                    stockCode = sslFile[:6]
                    stockSellList.append(stockCode)
                    #print("Code :: " + str(stockCode) + " ---")
                    #print(dataLines[0])
                    #print(last2ndLine)
                    #print(lastLine)
                    #print("==============================================\n")
                    
    return stockBuyList,stockSellList

def selectStock(currentDir):
    #csvDir = currentDir + "/csv/"
    ampDir = currentDir + "/amp"
    sslDir = currentDir + "/ssl"
    poolDir = currentDir + "/pool"
    
    today = time.strftime("%Y-%m-%d", time.localtime())
    
    print("******start picking stocks by amplitude ...")
    print("##############################################")
    candidatesList = selectByAMP(ampDir, 0.03)
    new_candidates = []
    last_amp = []
    if (len(candidatesList) > 0):
        try:
            f_pool_date = open(os.path.join(poolDir, "latest"),'r')
            last_update = f_pool_date.readline().strip()
            f_pool_date.close()
            if today == last_update:
                print(u"[INFO] 本次没有更新")
            else:
                f_amp = open(os.path.join(poolDir, "amp_" + last_update + ".csv"),'r')
                last_amp = f_amp.readline().split(',')
                #print(last_amp)
                for code in candidatesList:
                    if code not in last_amp:
                        new_candidates.append(code)
                f_new_amp = open(os.path.join(poolDir, "amp_" + today + ".csv"),'w')
                f_new_amp.write(','.join(candidatesList))

                f_pool_date = open(os.path.join(poolDir, "latest"),'w')
                f_pool_date.write(today.strip())
                f_pool_date.close()

                f_amp.close()
                f_new_amp.close()
            
        except:
            print("[ERROR] Failed to access file.")
            
        print(u"活跃度选股，以下是较活跃股票 - 当日振幅大于3%：")
        print(candidatesList)
        print(u"以下新增活跃股票 - 当日振幅大于3%：")
        print(new_candidates)
    print("##############################################\n")
    
    print("******start picking stocks by SSL ...")
    print("##############################################")
    buyList,sellList = selectBySSL(sslDir)
    if (len(buyList) > 0):
        print(u"趋势选股，以下是考虑买入的股票，理由向上突破压力：")
        print(buyList)
    print("==============================================\n")
    if (len(sellList) > 0):
        print(u"趋势选股，以下是考虑卖出的股票，理由向下跌破支撑：")
        print(sellList)
    print("##############################################\n")

if __name__ == "__main__":
    currentDir = os.getcwd()
    print("[INFO] Current working directory is: %s " % (currentDir))
    
    selectStock(currentDir)

       
