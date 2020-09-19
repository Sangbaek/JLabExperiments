#!/usr/bin/env python

"""
Writer: Sangbaek Lee (sangbaek@mit.edu)
The purpose of the code is to draw height of coins measured by each student.
The structure of the code is the same with drawCoinVolume.py.
I removed some unnecessary lines and comments on purpose to shorten the code.
This time, I'm keeping essential parts of main code by separating library part into a separate module.
Ref: https://docs.python.org/3/tutorial/modules.html
"""

from utils.studentData import * # This is the module I'd like to use.

studentData = studentData("data/coinData.dat", 1)

fig = plt.figure(figsize=(16,6))
fig.suptitle("Measured coin heights by 8.13 MWPM students")

ax1 = fig.add_subplot(121)	
ax1.set_title("Unbinned data")
ax1.set_xlabel('Coin height (cm)')
ax1.set_ylabel('Student Name')

dummyArray = np.arange(0,len(studentData.studentName),1) + 1
studentData.unitConversion()

quarterLabel = 0
pennyLabel = 0
for i, coinType in enumerate(studentData.coinType):
	if coinType == 'quarter': 		#Draw quarters.
		if (quarterLabel == 0):		#comes with legend only one time
			ax1.errorbar(studentData.coinHeight[i], dummyArray[i], xerr=studentData.coinHeightUncertainty[i]
				, marker='.',color='blue',markersize=5,capsize=3,lw=2, label='quarters')
			quarterLabel += 1
		else:						#otherwise don't set up a legend (quarters)
			ax1.errorbar(studentData.coinHeight[i], dummyArray[i], xerr=studentData.coinHeightUncertainty[i]
				, marker='.',color='blue',markersize=5,capsize=3,lw=2)
	if coinType == 'penny':			#Draw penny
		if (pennyLabel == 0):		#comes with legend only one time
			ax1.errorbar(studentData.coinHeight[i], dummyArray[i], xerr=studentData.coinHeightUncertainty[i]
				, marker='.',color='red',markersize=5,capsize=3,lw=2, label='pennies')
			pennyLabel += 1
		else:						#otherwise don't set up a legend (pennies)
			ax1.errorbar(studentData.coinHeight[i], dummyArray[i], xerr=studentData.coinHeightUncertainty[i]
				, marker='.',color='red',markersize=5,capsize=3,lw=2)

plt.legend(bbox_to_anchor=(0.95, 0.9), loc=1, title='Coin type',
            ncol=1, borderaxespad=0., handlelength=0.8)

ax1.set_xlim(0.05, .35)
ax1.set_ylim(0.5, len(studentData.studentName)+0.5)

# Set the ticks of axes.
xticks_major 	= np.arange(0.05, .351, 0.05)					# manually set up a major ticks
xticks_minor 	= np.arange(0.05, .351, 0.01)					# minor ticks
xticklabels 	= ['0.05','0.1','0.15','0.2','0.25','0.3','0.35']
ax1.set_xticks(xticks_major)								# apply major x ticks,
ax1.set_xticks(xticks_minor, minor=True)					# minor x ticks
ax1.set_xticklabels(xticklabels)							# , and x tick labels.

ax1.set_yticks(dummyArray)									# Lucky! just recycle dummyArray for y tick
ax1.set_yticklabels(deepcopy(studentData.studentName))				# apply y tick labels


# End of unbinned data plotting.
# Start of binned data plotting.
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
ax2.set_xlabel('Coin height (cm)')
ax2.set_ylabel('Number of Entries')

count, binEdges = 	np.histogram(studentData.coinHeight, np.arange(.1, .3, 0.025))
bincenters 		=	0.5*(binEdges[1:]+binEdges[:-1])
countStd		=	np.sqrt(count)
binwidth		=	binEdges[1] - binEdges[0]

ax2.hist(studentData.coinHeight, binEdges, color = 'b')

for i, freq in enumerate(count):
	if freq > 0:
		# ax2.errorbar(bincenters[i], count[i], xerr=binwidth/2., yerr=countStd[i], color='k', marker='.', markersize=5,capsize=3,lw=2)
		ax2.errorbar(bincenters[i], count[i], yerr=countStd[i], color='k', marker='.', markersize=5,capsize=3,lw=2)

# Set the limits of axes.
ax2.set_xlim(.1, .33)
ax2.set_ylim(0, 8)

# Set the ticks of axes.
xticks_major 	= np.arange(0.1, .33, 0.05)					# manually set up a major ticks
xticks_minor 	= np.arange(0.1, .33, 0.01)					# minor ticks
xticklabels 	= ['0.1','0.15','0.2','0.25','0.3']
ax2.set_xticks(xticks_major)								# apply major x ticks,
ax2.set_xticks(xticks_minor, minor=True)					# minor x ticks
ax2.set_xticklabels(xticklabels)							# , and x tick labels.
ax2.set_yticks([0, 1, 2, 3, 4, 5, 6, 7, 8])							
ax2.set_yticklabels(['0', '1', '2', '3', '4', '5', '6', '7', '8'])				# apply y tick labels

# Remove all margins!
plt.tight_layout()

# save plot for later viewing
plt.savefig("plots/coinHeight.png",bbox_inches='tight',dpi=400)

# show plots
plt.show()