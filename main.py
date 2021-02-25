from scipy.signal import argrelextrema
import numpy as np
import yfinance as yf
import datetime as dt
import pandas as pd
from finta import TA
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
symbol = "SBIN.NS"

def get_intra_data(symbol):
    daily = yf.download(tickers=symbol,  interval="15m", start = dt.datetime(2021,2,1),end = dt.datetime(2021,2,22))
    daily.index = daily.index.tz_localize(None)
    daily.drop(["Adj Close", 'Volume'], axis=1, inplace=True)
    daily["pre_close"] = daily['Close'].shift(1)
    daily["pre_low"] = daily['Low'].shift(1)
    daily["pre_high"] = daily['High'].shift(1)
    # daily = daily.ffill()
    # daily['sig'] = daily['minema']- daily['hourema']
    return daily



df = get_intra_data(symbol)

y1 = df.loc[:, 'High'].values
x = np.array([i for i in range(1, len(y1) + 1)])
peaks1, _ = find_peaks(y1)
plt.plot(peaks1, y1[peaks1], "x")
# y1[peaks1]

y2 = df.loc[:, 'Low'].values * -1
x = np.array([i for i in range(1, len(y1) + 1)])
peaks2, _ = find_peaks(y2)
plt.plot(peaks2, y2[peaks2] * -1, "x")
# y2[peaks2]*-1

# this way the   x-axis corresponds to the index of x
y = df.loc[:, 'Close'].values
plt.plot(x - 1, y)
# #
for x1 in x:
    plt.vlines(x=x1, ymin=min(y2 * -1), ymax=max(y1), colors='green', ls=':', lw=1)

for x1 in y1[peaks1]:
    plt.hlines(y=x1, xmin=min(x), xmax=max(x), colors='red', ls=':', lw=1)

for x1 in y2[peaks2] * -1:
    plt.hlines(y=x1, xmin=min(x), xmax=max(x), colors='green', ls=':', lw=1)



pos = 0
i = 0
for e in df.index:
    # searching for signal
    if i in peaks1:
        h1 =
    if dt.datetime(2020,2,2,9,15).time() <= e.time() <= dt.datetime(2020,2,2,14,30) and pos == 0 :


    if pos == 1:






