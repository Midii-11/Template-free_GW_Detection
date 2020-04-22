#!/usr/bin/env python3

from gwpy.timeseries import TimeSeries
import time

def pretty(t):
    return time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(t))

start=1126259446
end=1126259478
print(pretty(start), pretty(end))
hdata = TimeSeries.fetch_open_data('H1', start, end, cache=True)
print(hdata)

ser=[]


from matplotlib import pyplot as plt
for i in range(0,10):
    s=start+(end-start)*i
    e=start+(end-start)*(i+1)
    ser.append(TimeSeries.fetch_open_data('H1', s, e, cache=True).asd())
    plt.plot(ser[i], label='{0}-{1}'.format(s, e))

# from gwpy.plot import Plot

# plot=Plot(ser, linewidth=1)
# ax=plot.gca()
# ax.set_xlim(0,20)
plt.xlim((0,20))
plt.legend()
plt.show()
