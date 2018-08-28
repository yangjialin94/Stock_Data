'''
@author: Jialin Yang
@Date: 07/27/2018
@Lab: Final Project
@Course: 513
@Description: file to create DB tables and executions.
'''

import sqlite3

# function to create tables
def createTables():
	# connect to DB
	conn = sqlite3.connect('finalProject.db')
	cur = conn.cursor()

	# create userlist table if not exit
	conn.execute('''
		CREATE TABLE IF NOT EXISTS userlist
		(ID INTEGER PRIMARY KEY NOT NULL,
		USERNAME TEXT NOT NULL,
		PASSWORD TEXT NOT NULL,
		EMAIL TEXT NOT NULL,
		UNIQUE (USERNAME, PASSWORD, EMAIL));
		''')
	print("\nDB table userlist created")

	# create stockdata table
	conn.execute('''
		CREATE TABLE IF NOT EXISTS stockdata
		(ID INTEGER PRIMARY KEY NOT NULL,
		_DATE TEXT NOT NULL,
		_OPEN REAL NOT NULL,
		HIGH REAL NOT NULL,
		LOW REAL NOT NULL,
		CLOSE REAL NOT NULL,
		VOLUME REAL NOT NULL);
		''')
	print("\nDB table stockdata created")

# function to delete stockdata table
def deleteStockdataTables():
	# connect to DB
	conn = sqlite3.connect('finalProject.db')
	cur = conn.cursor()

	# create userlist table if not exit
	conn.execute("DROP TABLE IF EXISTS stockdata")
	print("\nDB table stockdata dropped")

# funtion to insert list of data to table
def insertAllData(dataList):
	# go over list
	for x in dataList:
		insertData(x[0], x[1], x[2], x[3], x[4], x[5])

	print("\ndata from dataList inserted")

# funtion to add data to table
def insertData(_date, _open, high, low, close, volume):
	# connect to DB
	conn = sqlite3.connect('finalProject.db')
	sql = "INSERT INTO stockdata (_DATE,_OPEN,HIGH,LOW,CLOSE,VOLUME) VALUES (?, ?, ?, ?, ?, ?)"
	data = (_date, _open, high, low, close, volume)
	cur = conn.cursor()

	# perform with error trapping 
	try:
		cur.execute(sql, data)
		conn.commit()
		# print("\ndata on date", _date, "inserted")
	except Exception as e:
		print("ERROR:", e)

	# close DB connection
	conn.close()


