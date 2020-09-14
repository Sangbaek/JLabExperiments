#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mlp

from optparse import OptionParser

# initial settings
mlp.rcParams['axes.linewidth'] = 2

#---------------------------------------------------------------------------------------------------
def readDataFromFile(file_name): 
        
    # arrays for x and y values
    xs = []
    dxs = []
    ys = []
    dys = []

    # read all data in one shot
    with open(file_name,"r") as file:
        data = file.read()

    # go through each row
    for line in data.split("\n"):
        f = line.split(',')                          # use a comma to separate columns
        if len(f)>3 and line[0] != '#':              # protect against not well formatted lines
            xs.append(float(f[0]))
            dxs.append(float(f[1]))
            ys.append(float(f[2]))
            dys.append(float(f[3]))

    return (xs,dxs,ys,dys)

#---------------------------------------------------------------------------------------------------
# define and get all command line arguments
parser = OptionParser()
parser.add_option("-n", "--name",  dest="name",  default='graph_xdxydy',   help="name of plot")
parser.add_option("-x", "--xtitle",dest="xtitle",default='Default x title',help="x axis title")
parser.add_option("-y", "--ytitle",dest="ytitle",default='Default y title',help="y axis title")
(options, args) = parser.parse_args()

# get my data
(xs,dxs,ys,dys) = readDataFromFile(options.name+".dat")

# define the figure
plt.figure(options.name)
plt.scatter(xs, ys, label = 'default curve')      # markers
plt.errorbar(xs,ys,xerr=dxs,yerr=dys,ls='none')   # error bars

# make axis titles
plt.xlabel(options.xtitle, fontsize=18)
plt.ylabel(options.ytitle, fontsize=18)

# make axis tick numbers larger
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# legend
leg = plt.legend(loc="lower left",frameon=False)

# make sure to not have too much white space around the plot
plt.subplots_adjust(top=0.99, right=0.99, bottom=0.13, left=0.12)

# save plot for later viewing
plt.savefig(options.name+".png",bbox_inches='tight',dpi=400)

# save plot for later viewing
plt.savefig(options.name+".png",bbox_inches='tight',dpi=400)

# show the plot for interactive use
plt.show()
