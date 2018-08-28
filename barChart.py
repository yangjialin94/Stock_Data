'''
@author: Jialin Yang
@Date: 07/27/2018
@Lab: Final Project
@Course: 513
@Description: class to generate bar chart.
'''

import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

class barChart():

    # Default constructor
    def __init__(self, x, y, xLabel, yLabel, year):
        self.x = [int(i) for i in x]
        self.y = y
        self.xLabel = xLabel
        self.yLabel = "Avg. " + yLabel
        self.title = str(year) + ": Avg. " + yLabel + " vs. " + xLabel + " Bar Chart"
        print("\n", self.title, sep="")

    # show scatter chart
    def showChart(self):
        # get avg y values/new y data
        avgY = []
        curY = []

        for i in range(len(self.y) - 1):
            curY.append(self.y[i])
            if self.x[i] != self.x[i + 1]:
                avgY.append(sum(curY) / len(curY))
                curY = []

        curY.append(self.y[len(self.y) - 1])
        avgY.append(sum(curY) / len(curY))
        self.y = avgY

        # get new x data
        newX = []

        for i in range(len(self.x) - 1):
            if self.x[i] != self.x[i + 1]:
                newX.append(self.x[i])

        newX.append(max(newX)+1)
        self.x = newX

        print(self.x)

        # Visualize Results
        plt.close(self.title)
        plt.figure(self.title)
        plt.bar(self.x, self.y, align='center')
        plt.title(self.title)
        plt.xlabel(self.xLabel)
        plt.ylabel(self.yLabel)
        plt.xticks(np.arange(min(self.x), max(self.x)+1, 1.0))
        plt.show(self.title)
