'''
@author: Jialin Yang
@Date: 07/27/2018
@Lab: Final Project
@Course: 513
@Description: class to save stock data into json file and funcitons to read stock data.
'''

import json
from datetime import datetime
from iexfinance import get_historical_data

class getData():

	# Default constructor
    def __init__(self, company, startYear, startMonth, startDay, endYear, endMonth, endDay):
        self.company = company
        self.startYear = startYear
        self.startMonth = startMonth
        self.startDay = startDay
        self.endYear = endYear
        self.endMonth = endMonth
        self.endDay = endDay
        self.data = []
        self.dataList = []

    # main file to get stock data for a day
    def getDailyStockData(self):
        # get stock price
        startDate = datetime(self.startYear, self.startMonth, self.startDay)
        endDate = datetime(self.endYear, self.endMonth, self.endDay)
        data = get_historical_data(self.company, start=startDate, end=endDate, output_format='json')
        data = data[self.company]

        # dump json data into file
        print("\nStart saving data saved to file.")
        with open('stockData.json', 'w') as file:
            json.dump(data, file, indent=4)
        print("Data saved to file.")

        # store data into list, format: [year-month-day, open, high, low, close, volume]
        for date, dataSet in data.items():
            self.data.append(date)
            for key, value in dataSet.items():
                self.data.append(value)

	# funciton to get stock data for a peiod of time
    def getStockData(self):
        # get StockPrice from startMonth-startDay-startYear to today's date
        now = datetime.now()
        month = now.month
        day = now.day 
        year = now.year

        # get stock price
        startDate = datetime(self.startYear, self.startMonth, self.startDay)
        endDate = datetime(self.endYear, self.endMonth, self.endDay)
        data = get_historical_data(self.company, start=startDate, end=endDate, output_format='json')
        data = data[self.company]

        # dump json data into file
        print("\nStart saving data saved to file.")
        with open('stockData.json', 'w') as file:
            json.dump(data, file, indent=4)
        print("Data saved to file.")

        # store data into list, format: [year-month-day, open, high, low, close, volume]
        for date, dataSet in data.items():
            newList = [date]
            for key, value in dataSet.items():
                newList.append(value)
            self.dataList.append(newList)



