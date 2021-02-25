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
    daily = yf.download(tickers=symbol,  interval="5m", period = "30d")
    daily.index = daily.index.tz_localize(None)
    daily.drop(["Adj Close", 'Volume'], axis=1, inplace=True)
    # daily = daily.ffill()
    # daily['sig'] = daily['minema']- daily['hourema']
    return daily

def get_dates(symbol):
    daily = yf.download(tickers=symbol, interval="1d", period = "30d")
    daily.index = daily.index.tz_localize(None)
    daily.drop(["Adj Close", 'Volume'], axis=1, inplace=True)
    return daily

def get_peaks(today):
    y1 = today.loc[:, 'High'].values
    x = np.array([i for i in range(1, len(y1) + 1)])
    peaks1, _ = find_peaks(y1)


    y2 = today.loc[:, 'Low'].values * -1
    x = np.array([i for i in range(1, len(y1) + 1)])
    peaks2, _ = find_peaks(y2)
    return y1,y2,peaks1,peaks2

def get_plot(y1,y2,peaks1,peaks2,df):
    plt.plot(peaks1, y1[peaks1], "x")
    plt.plot(peaks2, y2[peaks2] * -1, "x")
    y = df.loc[:, 'Close'].values
    x = np.array([i for i in range(1, len(y1) + 1)])
    plt.plot(x - 1, y)
    for x1 in peaks1:
        plt.vlines(x=x1, ymin=min(y2 * -1), ymax=max(y1), colors='green', ls=':', lw=1)
    for x1 in peaks2:
        plt.vlines(x=x1, ymin=min(y2 * -1), ymax=max(y1), colors='green', ls=':', lw=1)

    for x1 in y1[peaks1]:
        plt.hlines(y=x1, xmin=min(x), xmax=max(x), colors='red', ls=':', lw=1)

    for x1 in y2[peaks2] * -1:
        plt.hlines(y=x1, xmin=min(x), xmax=max(x), colors='green', ls=':', lw=1)

def get_today(df,symbol,date):
    return df[df.index.date == date]


percen = []
df = get_intra_data(symbol)
dates = list(get_dates(symbol).index.date)
for date in dates:
    print("########## new day")
    today = get_today(df,symbol,date)
    y1,y2,peaks1,peaks2 = get_peaks(today)
    pos = 0
    i = 0
    flag = 0
    h1 =0
    l1 =0
    # percen = []
    sl = 99999
    for e in today.index:
        # searching for signal
        if i in peaks1 :
            h1 = y1[i]
        if i in peaks2 :
            l1 = y2[i]*-1
        if (h1 == 0 or l1 == 0):
            i = i + 1
            # flag = 1
            continue

        if pos == 0 and today.loc[e,'High'] > h1:
            bp = h1
            sl = l1
            pos = 1
            print(f"buyed at {bp} time {e} and sl at {sl}")
            i = i + 1
            continue
        if pos == 1 and today.loc[e,'Low'] <= sl:
            sp = sl
            per = (sp/bp-1)*100
            print(f"TSL hit {sp} time {e}")
            percen.append(per)
            pos = 0
        if l1 > sl and pos == 1:
            sl = l1
            print(f"sl trailed to {sl}")
        if pos == 1 and e.time() == dt.datetime(2020,2,2,15,15) :
            sp = today.loc[e,'Open']
            per = (sp / bp - 1) * 100
            print(f"Sold at {sp}")
            percen.append(per)
            pos = 0
        i = i + 1
    # print(sum(percen))


sum(percen)
get_plot(y1,y2,peaks1,peaks2,today)