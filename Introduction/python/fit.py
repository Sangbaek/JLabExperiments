#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mlp

from scipy.stats import norm
from scipy.optimize import curve_fit

from optparse import OptionParser

g_norm = 1.0/np.sqrt(2*np.pi)


#---------------------------------------------------------------------------------------------------
# define and get all command line arguments
parser = OptionParser()
parser.add_option("-n", "--name",  dest="name",  default='fit',            help="name of plot")
parser.add_option("-x", "--xtitle",dest="xtitle",default='Default x title',help="x axis title")
parser.add_option("-y", "--ytitle",dest="ytitle",default='Default y title',help="y axis title")
(options, args) = parser.parse_args()

def straight_mean_var(data):
    # mean and variance from the raw data
    mean_raw = np.mean(data)
    var_raw = np.var(data)
    print "\n-- No fit"
    print " Nevents:  %d"%(len(data))
    print " Mean:     %f +- %f"%(np.mean(data),np.sqrt(np.var(data)/len(data)))
    print " Variance: %f"%(np.var(data))
    print " Width:    %f"%(np.sqrt(np.var(data)))

    return mean_raw,var_raw


def gaussian(x, amplitude, mean, width):
    # Gaussian function, including a variable normalization, ready for your histogram fit

    return amplitude*g_norm/width * np.exp(-0.5*((x-mean)/width)**2)

def fit_gaussian_without(xs,ys):
    # implement a set of histogram fits
    
    x_array = np.array(xs)
    y_array = np.array(ys)

    # fit without uncertainties
    pname = ['Amplitude', 'Mean', 'Width']
    par, pcov = curve_fit(gaussian, x_array, y_array, p0=(500, 10, 2))
    print "\n== Fit without including uncertainties"
    for i in range(0,3):
        print " P(%9s,%d): %f +- %f"%(pname[i],i,par[i],np.sqrt(pcov[i][i]))

    return par, pcov

def fit_gaussian(xs,ys):
    # implement a set of histogram fits
    
    x_array = np.array(xs)
    y_array = np.array(ys)

    # find uncertainties (simply sqrt of entries)
    sigma = np.sqrt(y_array)
    for i in range(0,len(sigma)): # if there are zero entries we get division by zero!
        if sigma[i] == 0:
            sigma[i] = 100
            #print " fix zero i:%d"%(i) 
    
    # fit with uncertainties
    print "\n== Fit including uncertainties"
    pname = ['Amplitude', 'Mean', 'Width']
    par, pcov = curve_fit(gaussian, x_array, y_array, p0=(500, 10, 2), sigma=sigma)
    for i in range(0,3):
        print " P(%9s,%d): %f +- %f"%(pname[i],i,par[i],np.sqrt(pcov[i][i]))

    return par, pcov

n_events = 500

# generate some data for this demonstration.
data = norm.rvs(10.0, 2.5, size=n_events)

# calculate variables
mean_raw,var_raw = straight_mean_var(data)

# define the figure
plt.figure(options.name)
ns, bins, patches = plt.hist(data, 25, histtype = 'step', linewidth=2)

# careful bin width matters for integral
binwidth = bins[1]-bins[0]
normalize = n_events * binwidth

# plot the prediction on top
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = normalize * norm.pdf(x, mean_raw, np.sqrt(var_raw)) # make sure to normalize correctly
label = "mu= %.2f, std= %.2f" % (mean_raw, np.sqrt(var_raw))
plt.plot(x, p, 'r', linewidth=2, label=label)
# legend
leg = plt.legend(loc="upper left",frameon=False)

# prepare data for the least chi2 binned fit
xs = []
ys = []
for n,bmin in zip(ns,bins[:-1]):
    xs.append(bmin+0.5*binwidth)
    ys.append(n)

# now fit the data
fit_gaussian_without(xs,ys)
fit_gaussian(xs,ys)

# make plot nicer
plt.xlabel(options.xtitle, fontsize=18)
plt.ylabel(options.ytitle, fontsize=18)

# make axis tick numbers larger
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# make sure to noe have too much white space around the plot
plt.subplots_adjust(top=0.99, right=0.99, bottom=0.13, left=0.12)

# save plot for later viewing
plt.savefig(options.name+".png",bbox_inches='tight',dpi=400)

# show the plot for interactive use
plt.show()

