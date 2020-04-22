#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
# Copyright (c) 2017 Duncan Macleod
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

"""Download and plot public LIGO data containing the GW150914 signal in both
detectors, including filtering to remove extraneous noise, on a transparent
background
This script was originally designed to generate a plot on the cover slide
for my presentation at PyCon UK 2017
"""

from gwpy.timeseries import TimeSeries
from gwpy.signal import filter_design
from gwpy.plot import (rcParams, TimeSeriesPlot)

rcParams.update({
    'figure.dpi': 600,
    'figure.subplot.left': 0.,
    'figure.subplot.right': 1.,
    'figure.subplot.bottom': 0.,
    'figure.subplot.top': 1.,
})

# get data
lho = TimeSeries.fetch_open_data('H1', 1126259446, 1126259478)
llo = TimeSeries.fetch_open_data('L1', 1126259446, 1126259478)

# design filter to extract signal
bp = filter_design.bandpass(50, 250, lho.sample_rate)
notches = [filter_design.notch(line, lho.sample_rate) for
           line in (60, 120, 180)]
zpk = filter_design.concatenate_zpks(bp, *notches)

# filter data
lhof = lho.filter(zpk, filtfilt=True).crop(1126259462, 1126259462.6)
llof = llo.filter(zpk, filtfilt=True).crop(1126259462, 1126259462.6)

# shift l1 data to account for time-delay and orientation
llof.t0 += 0.0069 * llof.t0.unit
llof *= -1 * llof.unit

# plot
plot = TimeSeriesPlot(figsize=[12, 4])
ax = plot.gca()
ax.plot(lhof, color='gwpy:ligo-hanford')
ax.plot(llof, color='gwpy:ligo-livingston')
ax.set_axis_off()
plot.show()