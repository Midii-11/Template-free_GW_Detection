#!/usr/bin/env python3

from gwpy.timeseries import TimeSeriesDict
from gwpy.plot import Plot

channels = [
    '{ifo}:ISI-BS_ST1_SENSCOR_GND_STS_X_BLRMS_30M_100M.mean,s-trend',
    '{ifo}:ISI-BS_ST1_SENSCOR_GND_STS_Y_BLRMS_30M_100M.mean,s-trend',
    '{ifo}:ISI-BS_ST1_SENSCOR_GND_STS_Z_BLRMS_30M_100M.mean,s-trend',
]
lho = TimeSeriesDict.get([c.format(ifo='H1') for c in channels],
                         'Feb 13 2015 16:00', 'Feb 14 2015 04:00')
llo = TimeSeriesDict.get([c.format(ifo='L1') for c in channels],
                         'Feb 13 2015 16:00', 'Feb 14 2015 04:00')

plot = Plot(lho, llo, figsize=(12, 6), sharex=True, yscale='log')
ax1, ax2 = plot.axes
for ifo, ax in zip(('Hanford', 'Livingston'), (ax1, ax2)):
    ax.legend(['X', 'Y', 'Z'])
    ax.text(1.01, 0.5, ifo, ha='left', va='center', transform=ax.transAxes,
            fontsize=18)
ax1.set_ylabel(r'$1-3$\,Hz motion [nm/s]', y=-0.1)
ax2.set_ylabel('')
ax1.set_title('Magnitude 7.1 earthquake impact on LIGO')
plot.show()
print("WTF")