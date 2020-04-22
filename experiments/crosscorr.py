#!/usr/bin/env python3

from gwpy.timeseries import TimeSeries
from gwpy.plot import Plot
import numpy as np
import matplotlib.pyplot as plt

def distance(a:TimeSeries,b:TimeSeries):
    am=a.mean()
    bm=b.mean()
    delta=bm-am
    ad=a+delta
    dist=np.zeros(len(a))
    xf=1000000
    xfi=1/xf
    ad=a.copy()
    bd=b.copy()

    thresh=10000000
    for i in range(len(a)):
        dist[i]=1/np.linalg.norm(a[i]-b[i])
        if dist[i]<-1E-6: 
            ad[i]=am
            bd[i]=bm
    return dist,ad,bd

# time=np.arange(0, 100, 0.1);
# a= TimeSeries(np.sin(time))
# b= TimeSeries(np.sin(time*1.5))


# plot=Plot([a,b, dist])
# plot.show()

hdata = TimeSeries.fetch_open_data('H1', 1126259446, 1126259478, cache=True)
ldata = TimeSeries.fetch_open_data('L1', 1126259446, 1126259478, cache=True)
d,hl,ll=distance(hdata, ldata)
print(d)
plot=Plot([hdata, ldata],d,[hl,ll])
plot.show()