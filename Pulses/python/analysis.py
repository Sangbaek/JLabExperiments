#!/usr/bin/env python

import sys
import pylandau
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mlp
from scipy.optimize import curve_fit

import ScopeTrace

merge_bins = 1

raw = True
plotting = True
fitting = True

#plotting = False
#fitting = False

def fit_pulse(trace):
    # fit the highest peak -> find the highest value
    x_array = np.array(trace.xvalues)
    y_array = np.array(trace.inverted())

    # find start value for position (if multiple max y values, selects the first)
    idx = np.where(y_array == y_array.max())
    idx = idx[0][0]
    #x_values_peak = x_array[idx]

    pname = [ 'Position','Amplitude','Width']
    mpv = x_array[idx]           # position of peak
    amp = y_array.max()          # height of peak
    width = 1                    # width of peak

    # The uncertainty on the y-values is assumed to be the same for each separate bin otherwise
    # you have to specify the uncertainties explicitely
    par, pcov = curve_fit(pylandau.landau, x_array, y_array, p0=(mpv, width, amp))

    plot_pulse(trace,baseline)
    plt.plot(x_array,mylandau(x_array,par[0],par[1],par[2]),label='Landau Fit')

    return pname, par, pcov

def mylandau(xvals,peak,width,ampl):
    # transform the input to the landau offered by the package and return the scaled values
    # mylandau has 3 parameters: peak position, peak width and peak amplitude
    nxvals = np.array([]) # n - refers to normalized values
    for xval in xvals:
        nxvals = np.append(nxvals,(xval-peak)/width)
    yvals = pylandau.landau(nxvals)

    return yvals * ampl

def plot_pulse(trace,baseline):

    # get x and y values of the traces
    recs = trace.xvalues
    adcs = trace.inverted()
    
    # define the figure
    fig = mlp.pyplot.gcf()
    fig.set_size_inches(18.5, 14.5)
    plt.figure(1)
    plt.plot(recs,adcs)
    
    # draw horizontal
    plt.axhline(y=0,color='b', linestyle='-', linewidth=2)
    
    # make plot nicer
    plt.xlabel('x-trace [n%s]'%trace.horizontal_units, fontsize=28)
    plt.ylabel('y-reading [%s]'%trace.vertical_units, fontsize=28)
    
    # tick marker sizes
    ax = plt.gca()
    ax.xaxis.set_tick_params(labelsize=16)
    ax.yaxis.set_tick_params(labelsize=20)
    
    ymin,ymax = ax.get_ylim()
    dy = ymax-ymin
    xmin,xmax = ax.get_xlim()
    dx = xmax-xmin
    plt.text(xmin-0.1*dx,ymin-0.05*dy, r'Source:  %s'%(trace.source), fontsize=20)
    
    # save plot for later viewing
    plt.subplots_adjust(top=0.99, right=0.99, bottom=0.10, left=0.10)
    #plt.show()

def plot_trace(trace):

    # get x and y values of the traces
    recs = trace.xvalues
    adcs = trace.yvalues
    
    # define the figure
    fig = mlp.pyplot.gcf()
    fig.set_size_inches(18.5, 14.5)
    plt.figure(1)
    plt.plot(recs,adcs)

    # tick marker sizes
    ax = plt.gca()
    ax.xaxis.set_tick_params(labelsize=16)
    ax.yaxis.set_tick_params(labelsize=20)
    
    ymin,ymax = ax.get_ylim()
    dy = ymax-ymin
    xmin,xmax = ax.get_xlim()
    dx = xmax-xmin
    plt.text(xmin-0.1*dx,ymin-0.05*dy, r'Source:  %s'%(trace.source), fontsize=20)
    
    # save plot for later viewing
    plt.subplots_adjust(top=0.99, right=0.99, bottom=0.10, left=0.10)
    
#---------------------------------------------------------------------------------------------------
# M A I N
#---------------------------------------------------------------------------------------------------
# initial settings
mlp.rcParams['axes.linewidth'] = 2

print(" Analysing: %d files as given in the command line"%(len(sys.argv[1:])))

for filename in sys.argv[1:]:

    # read the raw data
    print(" File: %s"%(filename))
    with open(filename,"r") as file:
        data = file.read()

    # decode the scope trace
    trace = ScopeTrace.ScopeTrace(data,merge_bins)
    x_array = np.array(trace.xvalues)
    if trace.reading_error>1 or len(trace.yvalues)<10:
        print(" WARNING -- skipping this file has reading errors: %s"%(filename))
        continue

    if raw:
        print(' Show the raw data.')
        plot_trace(trace)
        plt.show()

    # find baseline and jitter
    baseline,jitter = trace.find_baseline_and_jitter(0,250)
    
    print(' Filename: %s,  Baseline: %10.6f,  Jitter: %10.6f'%(filename,baseline,jitter))

    if plotting:
        print(' Show the data after finding a baseline and inverting the pulse.')
        plot_pulse(trace,baseline)
        plt.show()
        
    if fitting:
        print(' Perform a fit and determine the Landau distribution parameters.')
        pname, par, pcov = fit_pulse(trace)
        plt.show()
        print(" Fit results - Parameters: ")
        print(par)
        print(" Fit results - Covariance matrix: ")
        print(pcov)
        print(" ========================================")
        for i in range(0,len(par)):
            print(" P(%d,%9s) = %f +- %f"%(i,pname[i],par[i],np.sqrt(pcov[i][i])))
