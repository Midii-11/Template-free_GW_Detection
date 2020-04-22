#!/usr/bin/env python3

from gwpy.timeseries import TimeSeries
import time

def pretty(t):
    return time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(t))

def fetch(i=0, start=1126259446, delta=32):
    s,e=start+(delta*i), start+(delta*(i+1))
    print("Fetching data for {0} to {1}".format(pretty(s), pretty(e)))
    hdata = TimeSeries.fetch_open_data('H1', s, e, cache=True)
    ldata = TimeSeries.fetch_open_data('L1', s, e, cache=True)
    print("{0} points for H, {1} points for L".format(len(hdata), len(ldata)))
    return hdata, ldata

def filter_gwe(data:TimeSeries):
    bp = filter_design.bandpass(50, 250, data.sample_rate)
    notches = [filter_design.notch(line, data.sample_rate) for line in (60, 120, 180)]
    zpk = filter_design.concatenate_zpks(bp, *notches)
    filt = data.filter(zpk, filtfilt=True)
    data = data.crop(*data.span.contract(1))
    filt = filt.crop(*filt.span.contract(1))
    return data

recorded_events=



from gwpy.signal import filter_design
from gwpy.plot import Plot

import astropy.units as u
def zoom(ts:[TimeSeries], t, dt=0.5*u.s):
    print(t)
    plot2=Plot(ts)
    ax = plot2.gca()
    ax.set_xlim(t-dt, t+dt)
    plot2.show()

for i in range(10):
    hdata, ldata = fetch(i)
    
    plot=Plot(hfilt)
    maxx=hfilt.argmax(0)
    gt=(maxx*hfilt.dx)+hfilt.t0
    print("Peak observed at {0}, value {1} around {2}".format(maxx, hfilt[maxx], gt))
    plot.show()
    zoom((hfilt, hdata), gt)
