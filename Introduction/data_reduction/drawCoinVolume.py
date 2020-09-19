#!/usr/bin/env python

"""
Writer: Sangbaek Lee (sangbaek@mit.edu)
The first line is called the shebang line,
which makes you run this script as an executable in Unix system.
You can specify python versions with it too.
For my case, to use python3, I'd use
#!/usr/local/bin/python3
for python2, I'd use
#!/usr/bin/python2

You can get your python path by typing followings in your terminal.
which python
or 
which python2
"""

# This is one line comment.
# If you are more interested in docstring convention, please visit
# https://www.python.org/dev/peps/pep-0257/#:~:text=A%20docstring%20is%20a%20string,special%20attribute%20of%20that%20object.&text=String%20literals%20occurring%20elsewhere%20in%20Python%20code%20may%20also%20act%20as%20documentation.


# import some libraries
from __future__ import print_function #this allows python2 to have the same print function usage with python3
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



# Two ways to use this class.
# studentData = studentData("data/coinData.dat")
# studentData.readStudentData()
# or
studentData = studentData("data/coinData.dat", 1)
# which is equivalent with above two lines.

# Debug if everything is fine so far
for i, name in enumerate(studentData.studentName):
	print(studentData.studentName[i] +" measaured " + studentData.coinType[i] +' volume as '+str(studentData.coinVolume[i])+' +- '
		 + str(studentData.coinVolumeUncertainty[i]) + ' ' + studentData.coinVolumeUnit[i])

#Define the environment to draw plots
fig = plt.figure(figsize=(16,6))	#create a canvas, 24 inches by 6 inches
fig.suptitle("Measured coin volumes by 8.13 MWPM students")

#Often, it's useful to play with subplot on the canvas. 131 - 1 means number of rows, 3 means number of columns, the last 1 means that it's the first subplot
ax1 = fig.add_subplot(121)	

#Set subplot title and labels of axes.
ax1.set_title("Unbinned data")
ax1.set_xlabel('Coin volume (cm$^3$)')
ax1.set_ylabel('Student name')

#dummy y value for plotting
dummyArray = np.arange(0,len(studentData.studentName),1) + 1

# Now unify units for plotting.
studentData.unitConversion()

# Draw data by coin type
quarterLegend = 0
pennyLegend = 0
for i, coinType in enumerate(studentData.coinType):
	if coinType == 'quarter': 		#Draw quarters.
		if (quarterLegend == 0):		#comes with legend only one time
			ax1.errorbar(studentData.coinVolume[i], dummyArray[i], xerr=studentData.coinVolumeUncertainty[i]
				, marker='.',color='blue',markersize=5,capsize=3,lw=2, label='quarters')
			quarterLegend += 1
		else:						#otherwise don't set up a legend (quarters)
			ax1.errorbar(studentData.coinVolume[i], dummyArray[i], xerr=studentData.coinVolumeUncertainty[i]
				, marker='.',color='blue',markersize=5,capsize=3,lw=2)
	if coinType == 'penny':			#Draw penny
		if (pennyLegend == 0):		#comes with legend only one time
			ax1.errorbar(studentData.coinVolume[i], dummyArray[i], xerr=studentData.coinVolumeUncertainty[i]
				, marker='.',color='red',markersize=5,capsize=3,lw=2, label='pennies')
			pennyLegend += 1
		else:						#otherwise don't set up a legend (pennies)
			ax1.errorbar(studentData.coinVolume[i], dummyArray[i], xerr=studentData.coinVolumeUncertainty[i]
				, marker='.',color='red',markersize=5,capsize=3,lw=2)

# Locate the plot's legend.
plt.legend(bbox_to_anchor=(0.95, 0.9), loc=1, title='Coin type',
            ncol=1, borderaxespad=0., handlelength=0.8)


# Set the limits of axes.
ax1.set_xlim(0, 2)
ax1.set_ylim(0.5, len(studentData.studentName)+0.5)

# Set the ticks of axes.
xticks_major 	= np.arange(0, 2.00001, 0.2)					# manually set up a major ticks
xticklabels	 	= ["%.1f" % number for number in xticks_major] # don't want math fonts for tick labels. convert ticks to string array.
xticks_minor 	= np.arange(0, 2.00001, 0.05)					# minor ticks
ax1.set_xticks(xticks_major)								# apply major x ticks,
ax1.set_xticks(xticks_minor, minor=True)					# minor x ticks
ax1.set_xticklabels(xticklabels)							# , and x tick labels.
ax1.set_yticks(dummyArray)									# Lucky! just recycle dummyArray for y tick
ax1.set_yticklabels(deepcopy(studentData.studentName))		# apply y tick labels
# deepcopy is used here because we'll eventually remove penny row.
# deepcopy part is not trivial and not required for python3.
# For those interested, ref: https://www.geeksforgeeks.org/copy-python-deep-copy-shallow-copy/


# Done with unbinned data plotting.

# Now we're going to learn how to bin these data.
# Sadly, we need to drop penny data this time.

# Refs:
# 1. Bevington Ch. 4
# 2. https://en.wikipedia.org/wiki/Weighted_arithmetic_mean#Variance_weights
# 3. https://en.wikipedia.org/wiki/Inverse-variance_weighting
# 4. https://ned.ipac.caltech.edu/level5/Leo/Stats4_5.html
# 5. http://www.hep.uiuc.edu/e687/memos/weight_err.ps
# 6. https://suchideas.com/articles/maths/applied/histogram-errors/

studentData.dropPenny()

ax2 = fig.add_subplot(122)									# Another subplot to show unweighted histogram.

ax2.set_title("Binned data, unweighted")
ax2.set_xlabel('Coin volume (cm$^3$)')
ax2.set_ylabel('Number of Entries')

count, binEdges = 	np.histogram(studentData.coinVolume, np.arange(0.35, 0.9501, 0.1))
bincenters 		=	0.5*(binEdges[1:]+binEdges[:-1])
countStd		=	np.sqrt(count)
binwidth		=	binEdges[1] - binEdges[0]

ax2.hist(studentData.coinVolume, binEdges, color = 'b')

# Indicate error bars!
for i, freq in enumerate(count):
	if freq > 0:
		ax2.errorbar(bincenters[i], count[i], xerr = binwidth/2., yerr=countStd[i], color='k', marker='.', markersize=5,capsize=3,lw=2)

# Set the limits of axes.
ax2.set_xlim(0, 1.8)
ax2.set_ylim(0, 5)

# Set the ticks of axes.
xticks_major 	= np.arange(0, 1.81, 0.2)						# manually set up a major ticks
xticklabels	 	= ["%.1f" % number for number in xticks_major] 	# don't want math fonts for tick labels. convert ticks to string array.
xticks_minor 	= np.arange(0, 1.81, 0.05)						# minor ticks
ax2.set_xticks(xticks_major)								# apply major x ticks,
ax2.set_xticks(xticks_minor, minor=True)					# minor x ticks
ax2.set_xticklabels(xticklabels)							# , and x tick labels.
ax2.set_yticks([0, 1, 2, 3, 4, 5])							
ax2.set_yticklabels(['0', '1', '2', '3', '4', '5'])				# apply y tick labels

# Remove all margins!
plt.tight_layout()

# save plot for later viewing
plt.savefig("plots/coinVolume.png",bbox_inches='tight',dpi=400)

# show plots
plt.show()