#!/usr/bin/env python3

from gwpy.timeseries import TimeSeries
import time
from gwpy.time import tconvert
def pretty(t):
    return tconvert(t).strftime("%a, %d %b %Y %H:%M:%S %Z")

def fetch(i=0, start=1126259446, delta=32):
    halfdelta=delta/2
    s,e=start+(delta*i)-halfdelta, start+(delta*(i+1))-halfdelta
    print("Fetching data for {0} to {1}".format(pretty(s), pretty(e)))
    hdata = TimeSeries.fetch_open_data('H1', s, e, cache=True)
    ldata = TimeSeries.fetch_open_data('L1', s, e, cache=True)
    print("{0} points for H, {1} points for L".format(len(hdata), len(ldata)))
    return hdata, ldata

def filter_gwe(data:TimeSeries):
    from gwpy.signal import filter_design

    bp = filter_design.bandpass(50, 250, data.sample_rate)
    notches = [filter_design.notch(line, data.sample_rate) for line in (60, 120, 180)]
    zpk = filter_design.concatenate_zpks(bp, *notches)
    filt = data.filter(zpk, filtfilt=True)
    data = data.crop(*data.span.contract(1))
    filt = filt.crop(*filt.span.contract(1))
    return filt

recorded_events=[1126259462, 1128678900, 1135136350, 1167559936, 1180922494, 1185389807, 1186302519, 1186741861, 1187008882, 1187058327, 1187529256]

import matplotlib.pyplot as plt
for e in recorded_events:
    data=fetch(start=e, delta=8)[0]
    filt=filter_gwe(data)
    plt.subplot(3,1,1)
    plt.plot(data)
    plt.subplot(3,1,2)
    plt.plot(filt)
    plt.subplot(3,1,3)
    (data.spectrogram(3, fftlength=3, overlap=2) ** (1/2.)).plot()
    plt.show()