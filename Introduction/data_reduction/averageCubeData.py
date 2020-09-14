#!/usr/bin/env python
from __future__ import print_function 
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rc
from copy import deepcopy

class cubeData():
	""" using class is an efficient way to make your code clean
	"""
	def __init__(self, fname, read = 0):
		""" To read data from file.
		usage: cubeData = cubeData(fname, read = 1)
		"""
		self.usage = 'using class is a way to make your code clean'
		self.fname = fname
		self.file = open(fname, 'r')

		# Set up arrays to store data
		self.key = []
		self.id = []
		self.x = []
		self.dx = []
		self.y = []
		self.dy = []
		self.z = []
		self.dz = []
		self.v = []
		self.dv = []
		if (read == 1):
			self.readCubeData()

	def readCubeData(self):
		""" You can define methods working in the class.
		this method works like a function to read data from files.
		"""
		for i, line in enumerate(self.file): # read data from files.
			columns = line.split(',')
			#store data in predefined arrays
			self.key.append(columns[0])
			self.id.append(columns[1])
			self.x.append(float(columns[2]))
			self.dx.append(float(columns[3]))
			self.y.append(float(columns[4]))
			self.dy.append(float(columns[5]))
			self.z.append(float(columns[6]))
			self.dz.append(float(columns[7]))
			self.v.append(float(columns[8]))
			self.dv.append(float(columns[9]))
		self.file.close()

cubeData = cubeData("data/cubeData.csv", 1)

x	=	np.array(cubeData.x)
y   = 	np.array(cubeData.y)
z	= 	np.array(cubeData.z)
v	= 	np.array(cubeData.v)

dx	=	np.array(cubeData.dx)
dy  = 	np.array(cubeData.dy)
dz	= 	np.array(cubeData.dz)
dv	= 	np.array(cubeData.dv)

weight_x	=	1/dx/dx
weight_y	=	1/dy/dy
weight_z	=	1/dz/dz
weight_v	=	1/dv/dv

avg_x       =   np.sum(weight_x*x)/np.sum(weight_x)
avg_y       =   np.sum(weight_y*y)/np.sum(weight_y)
avg_z       =   np.sum(weight_z*z)/np.sum(weight_z)
avg_v		=	np.sum(weight_v*v)/np.sum(weight_v)

std_x		=	np.sqrt(1/np.sum(weight_x))
std_y		=	np.sqrt(1/np.sum(weight_y))
std_z		=	np.sqrt(1/np.sum(weight_z))
std_v		=	np.sqrt(1/np.sum(weight_v))

print("avg_x:	"+str(avg_x))
print("avg_y:	"+str(avg_y))
print("avg_z:	"+str(avg_z))
print("avg_v:	"+str(avg_v))
print("std_x:	"+str(std_x))
print("std_y:	"+str(std_y))
print("std_z:	"+str(std_z))
print("std_v:	"+str(std_v))
print("Now convert these numbers into some meaningful values!")
