#!/usr/bin/env python
#
# in linux this allows us to specify how the text below is evaluated. It uses
# python as provided by our environment. A little gnarly but one can get used
# to it.
#----------------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np

# Generate the Data for plotting in arrays t and s
t = np.arange(0.0, 2.0, 0.01)
s = 1 + np.sin(2 * np.pi * t)

# Define a plot area
fig, ax = plt.subplots()

# Assign the data to the plot
ax.plot(t,s)
ax.set(xlabel='time [s]',ylabel='voltage [mV]',title='As simple as it gets')

# Save the figure
fig.savefig('simple_plot.png')

# Show the plot that was created
plt.show()
