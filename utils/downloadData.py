# -*- coding: utf-8 -*-

import tushare as ts

#print ts._version__
#ts.get_hist_data('sh',start='2016-01-01').to_csv('d:/pythonws/traderlzl/csv/sh.csv')

#To get daily data for specified code, from start date to latest.
def getBasicData(stockCode, csvDir, startDate,endDate,kType):
    #save the csv file into .\\csv directory
    #print("[INFO] Downloading: stockCode = %s, startDate = %s" % (stockCode,startDate))
    #ts.get_hist_data(stockCode,start=startDate)
    data = ts.get_hist_data(code=stockCode,start=startDate,end=endDate,ktype=kType,retry_count=3,pause=1)
    if type(data) :
        data.to_csv(csvDir + stockCode + ".csv")
    else:
        print("[ERROR] failed to get data, real type is: %s" % (type(data)))

