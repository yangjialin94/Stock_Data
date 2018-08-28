'''
@author: Jialin Yang
@Date: 07/27/2018
@Lab: Final Project
@Course: 513
@Description: main file to process windows and menu driven system.
'''

import os
import ast
import time
import numpy as np

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import *

import dbTable
import getData
import generateAccessCode
import scatterChart
import barChart

# function direct from access frame to login frame
def accessToLoginFrame():
    accessRoot.destroy()
    loginFrame()

# function direct from login frame to access frame
def loginToAccessFrame():
    loginRoot.destroy()
    accessFrame()

# function direct from register frame to login frame
def registerToLoginFrame():
    registerRoot.destroy()
    loginFrame()

# function direct from login frame to main frame
def loginToMainFrame():
    loginRoot.destroy()
    mainFrame()

# function direct from main frame to login frame
def mainToLoginFrame():
    mainRoot.destroy()
    loginFrame()

# function to open analysis frame
def openAnalysisFrame():
    # check loading status
    if loaded:
        # direct to data frame
        analysisFrame()
    else:
        # show warning message
        messagebox.showwarning("ERROR", "Data not loaded. Please enter SYMBOL and YEAR to load data first.") 

# function to open data frame
def openDataFrame():
    # check loading status
    if loaded:
        # direct to data frame
        dataFrame()
    else:
        # show warning message
        messagebox.showwarning("ERROR", "Data not loaded. Please enter SYMBOL and YEAR to load data first.") 

# function to load scatter plot
def showScatter():
    # check loading status
    if loaded:
        # get yLabel
        yLabel = str(graphY.get())

        if yLabel == "OPEN":
            y = openList
        elif yLabel == "HIGH":
            y = highList
        elif yLabel == "LOW":
            y = lowList
        elif yLabel == "CLOSE":
            y = closeList
        else:
            y = volumeList

        # show scatter plot
        scatterChartObg = scatterChart.scatterChart(dateList, y, "DATE (MONTH)", yLabel, year)
        scatterChartObg.showChart()
    else:
        # show warning message
        messagebox.showwarning("ERROR", "Data not loaded. Please enter SYMBOL and YEAR to load data first.") 

# function to load higtogram():
def showBar():
    # check loading status
    if loaded:
        # get yLabel
        yLabel = str(graphY.get())

        if yLabel == "OPEN":
            y = openList
        elif yLabel == "HIGH":
            y = highList
        elif yLabel == "LOW":
            y = lowList
        elif yLabel == "CLOSE":
            y = closeList
        else:
            y = volumeList

        # show scatter plot
        barChartObg = barChart.barChart(dateList, y, "DATE (MONTH)", yLabel, year)
        barChartObg.showChart()
    else:
        # show warning message
        messagebox.showwarning("ERROR", "Data not loaded. Please enter SYMBOL and YEAR to load data first.") 

# funciton to get analysis data
def getAnalysis():
    # create list
    global analysisData
    analysisData = []

    # add lowest prices
    analysisData.append(["Lowest OPEN", np.min(openList), fullDateList[openList.index(np.min(openList))]])
    analysisData.append(["Lowest HIGH", np.min(highList), fullDateList[highList.index(np.min(highList))]])
    analysisData.append(["Lowest LOW", np.min(lowList), fullDateList[lowList.index(np.min(lowList))]])
    analysisData.append(["Lowest CLOSE", np.min(closeList), fullDateList[closeList.index(np.min(closeList))]])
    analysisData.append(["Lowest VOLUME", np.min(volumeList), fullDateList[volumeList.index(np.min(volumeList))]])

    # add medians
    analysisData.append(["Median OPEN", np.median(openList), "N/A"])
    analysisData.append(["Median HIGH", np.median(highList), "N/A"])
    analysisData.append(["Median LOW", np.median(lowList), "N/A"])
    analysisData.append(["Median CLOSE", np.median(closeList), "N/A"])
    analysisData.append(["Median VOLUME", np.median(volumeList), "N/A"])

    # add highst prices
    analysisData.append(["Highest OPEN", np.max(openList), fullDateList[openList.index(np.max(openList))]])
    analysisData.append(["Highest HIGH", np.max(highList), fullDateList[highList.index(np.max(highList))]])
    analysisData.append(["Highest LOW", np.max(lowList), fullDateList[lowList.index(np.max(lowList))]])
    analysisData.append(["Highest CLOSE", np.max(closeList), fullDateList[closeList.index(np.max(closeList))]])
    analysisData.append(["Highest VOLUME", np.max(volumeList), fullDateList[volumeList.index(np.max(volumeList))]])

# funciton to get data for specific date
def getDailyData():
    # error trapping: inputs, get data
    try:
        # parse year, month, day
        curDate = mainDate.get().strip().split("-")
        year = int(curDate[0])
        month = int(curDate[1])
        day = int(curDate[2])

        getDataObj = getData.getData(mainCompany.get().upper(), year, month, day, year, month, day)
        getDataObj.getDailyStockData()
        curStock = getDataObj.data
    except:
        # show warning message
        messagebox.showwarning("ERROR", "Invalid SYMBOL/DATE") 
    else:
        if curStock == []:
            # show warning message
            message = "Market not open on " + mainDate.get().strip()
            messagebox.showwarning("ERROR", message) 
        else:
            report = "DATE" + ": " + str(curStock[0]) + "\n" + \
                    "OPEN" + ": " + str(curStock[1]) + "\n" + \
                    "HIGH" + ": " + str(curStock[2]) + "\n" + \
                    "LOW" + ": " + str(curStock[3]) + "\n" + \
                    "CLOSE" + ": " + str(curStock[4]) + "\n" + \
                    "VOLUME" + ": " + str(curStock[5])

            # show warning message
            messagebox.showinfo(mainCompany.get().upper(), report)

# function to load company data
def loadCompany():
    global loaded, dataList, fullDateList, dateList, openList, highList, lowList, closeList, volumeList, year

    # error trapping: inputs, get data
    try:
        # get and save data
        getDataObj = getData.getData(mainCompany.get().upper(), int(mainYear.get()), 1, 1, int(mainYear.get()), 12, 31)
        getDataObj.getStockData()
        dataList = getDataObj.dataList
        year = dataList[0][0][:4]
    except:
        # show warning message
        messagebox.showwarning("ERROR", "Invalid SYMBOL/YEAR") 
    else:
        # insert datalist into DB table
        dbTable.insertAllData(dataList)

        # parse data into seprated list
        fullDateList = []
        dateList = []
        openList = []
        highList = []
        lowList = []
        closeList = []
        volumeList = []

        for x in dataList:
            fullDateList.append(x[0])
            dateList.append(x[0].replace("-", ".")[5:7])
            openList.append(x[1])
            highList.append(x[2])
            lowList.append(x[3])
            closeList.append(x[4])
            volumeList.append(x[5])

        # print to console
        loaded = True
        print("\nData Loaded:", mainCompany.get().upper())

# function to get access code by pin
def getAccessCode():
    valid = False

    # error trapping: accessPin
    try:
        getPin = int(accessPin.get())
        getAccessCode = ""
    except:
        # show warning message
        messagebox.showwarning("ERROR", "Invalid Pin") 
    else:
        # loop to get matching pair
        for accessCode, pin in tuples:
            if pin == getPin:
               getAccessCode = "Access Code: " + str(accessCode)
               valid = True

        # show result
        if valid:
            # show acccess code
            messagebox.showinfo("ACCESS CODE", getAccessCode)
            accessToLoginFrame()
        else:
            # show warning message
            messagebox.showwarning("ERROR", "Invalid Pin")

# function for login
def login():
    valid = False

    # error trapping: accessPin
    try:
        getPin = int(loginPin.get())
        getCode = int(loginCode.get())
    except:
        # show warning message
        messagebox.showwarning("ERROR", "Invalid Pin/Code Pair")
    else:
        # loop to get matching pair
        for accessCode, pin in tuples:
            if pin == getPin and accessCode == getCode:
                valid = True

        # show result
        if valid:
            loginToMainFrame()
        else:
            # show warning message
            messagebox.showwarning("ERROR", "Invalid Pin/Code Pair")

# function to exit program
def exit():
    # prompt message box
    if messagebox.askokcancel(title="Exit", 
        message="Do you really want to quit?") == 1:
        # delete DB table stockdata
        dbTable.deleteStockdataTables()

        # print out name, date/time, and lab number
        print("\nExit Program...")
        print("\nAuthor: Jialin Yang")
        print("Date:", time.strftime("%d/%m/%Y"))
        print("Current time:", time.strftime("%X"))
        print("Final Project\n")

        # exit
        os._exit(1)

# function to build analysis frame
def analysisFrame():
    # print to console
    print("\nAnalysis Window")

    # global variabels
    global analysisRoot

    # create root window
    analysisRoot = Tk()
    analysisRoot.title("Analysis Window")

    # create frame
    frame = Frame(analysisRoot)
    frame.pack()

    # get analysis data
    getAnalysis()

    # create treeview
    treeView = Treeview(frame)
    treeView['columns'] = ('VALUE', 'DATE')
    treeView.heading("#0", text='DESCRIPTION', anchor='center')
    treeView.column("#0", anchor="center", width=120)
    treeView.heading('VALUE', text='VALUE')
    treeView.column('VALUE', anchor='center', width=120)
    treeView.heading('DATE', text='DATE')
    treeView.column('DATE', anchor='center', width=120)
    treeView.grid(sticky = (N,S,W,E))

    for x in analysisData:     
        treeView.insert('', 'end', text=x[0], values=(x[1], x[2]))

    # exit until stop running
    analysisRoot.mainloop()


# function to build data frame
def dataFrame():
    # print to console
    print("\nData Window")

    # global variabels
    global dataRoot

    # create root window
    dataRoot = Tk()
    dataRoot.title(mainCompany.get().upper())

    # create frame
    frame = Frame(dataRoot)
    frame.pack()

    # create treeview
    treeView = Treeview(frame)
    treeView['columns'] = ('OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME')
    treeView.heading("#0", text='DATE', anchor='center')
    treeView.column("#0", anchor="center", width=100)
    treeView.heading('OPEN', text='OPEN')
    treeView.column('OPEN', anchor='center', width=100)
    treeView.heading('HIGH', text='HIGH')
    treeView.column('HIGH', anchor='center', width=100)
    treeView.heading('LOW', text='LOW')
    treeView.column('LOW', anchor='center', width=100)
    treeView.heading('CLOSE', text='CLOSE')
    treeView.column('CLOSE', anchor='center', width=100)
    treeView.heading('VOLUME', text='VOLUME')
    treeView.column('VOLUME', anchor='center', width=100)
    treeView.grid(sticky = (N,S,W,E))

    for x in dataList:     
        treeView.insert('', 'end', text=x[0], values=(x[1], x[2], x[3], x[4], x[5]))

    # exit until stop running
    dataRoot.mainloop()

# function to build register frame
def mainFrame():
    # print to console
    print("\nMain Window")

    # global variabels
    global mainRoot, mainCompany, mainDate, mainYear, dataList, graphY
    dataList = []

    # create root window
    mainRoot = Tk()
    mainRoot.title("Main Window")

    # create frame
    frame = Frame(mainRoot)
    frame.pack()

    # create labels and buttons
    mainCompany = StringVar()
    Label(frame, text="SYMBOL (ex.GOOG):").grid(row=0, column=0, sticky=E)
    Entry(frame, textvariable=mainCompany).grid(row=0, column=1, sticky=W)

    mainDate = StringVar()
    Label(frame, text="DATE (2017-12-25):").grid(row=1, column=0, sticky=E)
    Entry(frame, textvariable=mainDate).grid(row=1, column=1, sticky=W)
    Button(frame, text="GET", command=getDailyData).grid(row=1, column=2, sticky=W)

    Label(frame, text="or").grid(row=2, column=1)

    mainYear = StringVar()
    Label(frame, text="YEAR (≥2014):").grid(row=3, column=0, sticky=E)
    Entry(frame, textvariable=mainYear).grid(row=3, column=1, sticky=W)
    Button(frame, text="LOAD", command=loadCompany).grid(row=3, column=2, sticky=W)

    # create frame
    frame = Frame(mainRoot)
    frame.pack()

    # create option menu
    graphY = StringVar()
    options = ["OPEN", "HIGH", "LOW", "CLOSE", "VOLUME"]
    OptionMenu(frame, graphY, options[3], *options).pack(side=LEFT)

    # create labels
    Label(frame, text="vs.").pack(side=LEFT)
    Label(frame, text="DATE (MONTH)").pack(side=LEFT)

    # create buttons
    Button(frame, text="SCATTER", command=showScatter).pack(side=LEFT)
    Button(frame, text="BAR", command=showBar).pack(side=LEFT)

    # create more buttons
    frame = Frame(mainRoot)
    frame.pack()

    # create buttons
    Button(frame, text="DATA", command=openDataFrame).pack(side=LEFT)
    Button(frame, text="ANALYSIS", command=openAnalysisFrame).pack(side=LEFT)
    Button(frame, text="BACK", command=mainToLoginFrame).pack(side=LEFT)
    Button(frame, text="EXIT", command=exit).pack(side=LEFT)

    # exit until stop running
    mainRoot.mainloop()

# function to build access frame
def accessFrame():
    # print to console
    print("\nAccess Window")

    # global variabels
    global accessRoot, accessPin

    # create root window
    accessRoot = Tk()
    accessRoot.title("Access Window")

    # create frame
    frame = Frame(accessRoot)
    frame.pack()

    # create label and button
    accessPin = StringVar()
    Label(frame, text="Pin (1000-1020):").grid(row=0, column=0, sticky=E)
    Entry(frame, textvariable=accessPin).grid(row=0, column=1, sticky=W)

    # create frame
    frame = Frame(accessRoot)
    frame.pack()

    # create button
    Button(frame, text="BACK", command=accessToLoginFrame).pack(side=LEFT)
    Button(frame, text="GET ACCESS CODE", command=getAccessCode).pack(side=LEFT)

    # exit until stop running
    accessRoot.mainloop()

# function to build login frame
def loginFrame():
    # print to console
    print("\nLogin Window")

    # global variabels
    global loginRoot, loginPin, loginCode

    # create root window
    loginRoot = Tk()
    loginRoot.title("Login Page")

    # create frame
    frame = Frame(loginRoot)
    frame.pack()

    # create labels
    loginPin = StringVar()
    Label(frame, text="Pin:").grid(row=0, column=0, sticky=E)
    Entry(frame, textvariable=loginPin).grid(row=0, column=1, sticky=W)

    loginCode = StringVar()
    Label(frame, text="Code:").grid(row=1, column=0, sticky=E)
    Entry(frame, textvariable=loginCode).grid(row=1, column=1, sticky=W)

    # create frame
    frame = Frame(loginRoot)
    frame.pack()

    # create buttons
    accessBtn = Button(frame, text="GENERATE", command=loginToAccessFrame).pack(side=LEFT)
    loginBtn = Button(frame, text="LOGIN", command=login).pack(side=LEFT)
    exitBtn = Button(frame, text="EXIT", command=exit).pack(side=LEFT)

    # exit until stop running
    loginRoot.mainloop()

# start the program
if __name__ == '__main__':
    # global variable
    global tuples
    global loaded
    loaded = False

    # create DB tables
    dbTable.createTables()

    # generate code and save it inot list
    generateAccessCode.generateAccessCode()

    # read from file
    with open("users.dat", "r") as file:
        tuples = file.readline()

    file.close()
    tuples = ast.literal_eval(tuples)

    # start frame until exit
    loginFrame()




