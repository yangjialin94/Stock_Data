'''
@author: Jialin Yang
@Date: 07/27/2018
@Lab: Final Project
@Course: 513
@Description: file to generate random access code.
'''

import random

def generateAccessCode():

	file = open("users.dat", "w")
	file.write("[")

	for pin in range(1000, 1021):
		accessCode = random.randint(0, 10**5)

		cur = "(" + str(accessCode) + ", " + str(pin) + ")" + ","
		file.write(cur)

	file.write("]")
	file.close()