#!/usr/bin/env python3

import requests
from gwpy.timeseries import TimeSeries
import time
from gwpy.time import tconvert

def pretty(t):
    return tconvert(t).strftime("%a, %d %b %Y %H:%M:%S %Z")

def fetch(start=1126259446, delta=32, i=0, cache=True):
    halfdelta=delta/2
    s,e=start+(delta*i)-halfdelta, start+(delta*(i+1))-halfdelta
    print("Fetching data for {0} to {1}".format(pretty(s), pretty(e)))
    hdata = TimeSeries.fetch_open_data('H1', s, e, cache=cache)
    ldata = TimeSeries.fetch_open_data('L1', s, e, cache=cache)
    print("{0} points for H, {1} points for L".format(len(hdata), len(ldata)))
    return hdata, ldata

r = requests.get(url = 'https://www.gw-openscience.org/eventapi/html/allevents/')

import pandas as pd
import numpy as np

data=pd.read_html(r.text)[0]
print(data)

# print(data.iloc[:,[0,3,4,5,6]])
# for i,d in enumerate(data.iloc[:,3]):
#     try:
#         while True:
#             try:
#                 fetch(start=d, cache=True)
#                 break
#             except TimeoutError:
#                 print('Retrying...')
#     except ValueError:
#         print(f'Data for {pretty(d)} does not yet exist')

X=[]
Y=[]
for i,d in enumerate(data.iloc[:,3]):
    print(data.iloc[i,0])
    # if i == 4: break
    try:
        if 'GW' not in data.iloc[i,0]: continue
    except Exception as e:
        print(e) 
        continue
    try:
        for j in range(-50,50):
            h,l=fetch(start=d, i=j, cache=True)
            X.append([np.array(h), np.array(l)])
            Y.append(j==0)
    except ValueError: pass

X,Y=np.array(X),np.array(Y)
np.savez_compressed('x.npz',X)
np.savez_compressed('y.npz',Y)