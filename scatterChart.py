'''
@author: Jialin Yang
@Date: 07/27/2018
@Lab: Final Project
@Course: 513
@Description: class to generate scatter plot chart.
'''

import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression

class scatterChart():

	# Default constructor
    def __init__(self, x, y, xLabel, yLabel, year):
        self.x = [int(i) for i in x]
        self.y = y
        self.xLabel = xLabel
        self.yLabel = yLabel
        self.title = year + ": " + yLabel + " vs. " + xLabel + " Scatter Plot"
        print("\n", self.title, sep="")

    # show scatter chart
    def showChart(self):
        #Convert to 1d Vector for later plottings
        self.x = np.reshape(self.x, (len(self.x), 1))
        self.y = np.reshape(self.y, (len(self.y), 1))

        # Define Linear Regressor Object
        regressor = LinearRegression()
        regressor.fit(self.x, self.y)

        #Predict Price on Given Date (y, m or d)
        date = 12
        predicted_price =regressor.predict(date)

        #display summary stats
        print("Predicted", self.yLabel, predicted_price[0][0])
        print("Confidence ( % ) of data fit", regressor.score(self.x, self.y))

        # Visualize Results
        plt.close(self.title)
        plt.figure(self.title)
        plt.scatter(self.x, self.y, label='Actual ' + self.yLabel)
        plt.plot(self.x, regressor.predict(self.x), color='red', linewidth=3, label='Predicted ' + self.yLabel)
        plt.title(self.title)
        plt.xlabel(self.xLabel)
        plt.ylabel(self.yLabel)
        plt.xticks(np.arange(min(self.x), max(self.x)+1, 1.0))
        plt.legend()
        plt.show(self.title)

