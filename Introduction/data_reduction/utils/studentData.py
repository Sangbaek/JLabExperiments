from __future__ import print_function 
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rc
from copy import deepcopy

# initial settings
pgf_with_latex = {
		"pgf.texsystem": "pdflatex",
		"text.usetex": True,            # use LaTeX to write all text
		"font.family": "sans-serif",         
		"font.sans-serif": "Helvetica",
		"font.size": 15,				# default font size
		"axes.labelsize": 15,			# x and y label size
		"axes.titlesize": 25,           # subfigure title size, i.e. title size when one figure
		"legend.fontsize": 12,			# legend size
		"xtick.labelsize": 14,			# x axis tick label size
		"ytick.labelsize": 14,			# y axis tick label 
		"figure.titlesize": 35,         # Figure title size, useful when you have multiple plots in one canvas.
		"pgf.preamble": r"\usepackage{xcolor}"     # xcolor for colours
}
matplotlib.rcParams.update(pgf_with_latex)


class studentData():
	""" using class is an efficient way to make your code clean
	"""
	def __init__(self, fname, read = 0):
		""" To read data from file.
		usage: studentData = studentData(fname, read = 1)
		"""
		self.usage = 'using class is a way to make your code clean'
		self.fname = fname
		self.file = open(fname, 'r')

		# Set up arrays to store data
		self.studentName = []
		self.coinDiameter = []
		self.coinDiameterUncertainty = []
		self.coinDiameterUnit = []
		self.coinHeight = []
		self.coinHeightUncertainty = []
		self.coinHeightUnit = []
		self.coinVolume = []
		self.coinVolumeUncertainty = []
		self.coinType = []
		self.coinVolumeUnit = []
		if (read == 1):
			self.readStudentData()

	def readStudentData(self):
		""" You can define methods working in the class.
		this method works like a function to read data from files.
		"""
		for i, line in enumerate(self.file): # read data from files.
			columns = line.split('\t') #parse tab separated table. change delimiter accordingly.
			if (i==0):
				continue 			#skip the top row of the table and empty rows.
			#store data in predefined arrays
			self.studentName.append(columns[0])
			self.coinDiameter.append(float(columns[1]))
			self.coinDiameterUncertainty.append(float(columns[2]))
			self.coinDiameterUnit.append(columns[3])
			self.coinHeight.append(float(columns[4]))
			self.coinHeightUncertainty.append(float(columns[5]))
			self.coinHeightUnit.append(columns[6])
			self.coinVolume.append(float(columns[7]))
			self.coinVolumeUncertainty.append(float(columns[8]))
			self.coinVolumeUnit.append(columns[9])
			self.coinType.append(columns[10])
		self.file.close()

	def unitConversion(self):
		""" change mm^3 to cm^3
		change mm to cm
		"""
		for i, unit in enumerate(self.coinVolumeUnit):
			if unit == "mm^3":
				self.coinVolumeUnit[i] = "cm^3"
				self.coinVolume[i] = self.coinVolume[i] * 0.001
				self.coinVolumeUncertainty[i] = self.coinVolumeUncertainty[i] * 0.001

		for i, unit in enumerate(self.coinHeightUnit):
			if unit == "mm":
				self.coinHeightUnit[i] = "cm"
				self.coinHeight[i] = self.coinHeight[i] * 0.1
				self.coinHeightUncertainty[i] = self.coinHeightUncertainty[i] * 0.1

		for i, unit in enumerate(self.coinDiameterUnit):
			if unit == "mm":
				self.coinDiameterUnit[i] = "cm"
				self.coinDiameter[i] = self.coinDiameter[i] * 0.1
				self.coinDiameterUncertainty[i] = self.coinDiameterUncertainty[i] * 0.1

	def dropPenny(self):
		"""remove the penny row for drawing histogram
		"""
		penny_ind = self.coinType.index('penny')
		self.studentName.pop(penny_ind)
		self.coinDiameter.pop(penny_ind)
		self.coinDiameterUncertainty.pop(penny_ind)
		self.coinDiameterUnit.pop(penny_ind)
		self.coinHeight.pop(penny_ind)
		self.coinHeightUncertainty.pop(penny_ind)
		self.coinHeightUnit.pop(penny_ind)
		self.coinVolume.pop(penny_ind)
		self.coinVolumeUncertainty.pop(penny_ind)
		self.coinVolumeUnit.pop(penny_ind)
		self.coinType.pop(penny_ind)