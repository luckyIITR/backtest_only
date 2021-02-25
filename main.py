from scipy.signal import argrelextrema
import numpy as np
import yfinance as yf
import datetime as dt
import pandas as pd
from finta import TA
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
# symbol = "HDFCBANK.NS"
def main(symbol):
    global p_l
    def get_intra_data(symbol):
        daily = yf.download(tickers=symbol,  interval="15m", period="30d")
        daily["hourema"] = TA.EMA(yf.download(tickers=symbol, interval="60m", period="60d"),50)
        daily["minema"] =  TA.EMA(yf.download(tickers=symbol, interval="15m", period="60d"),50)
        daily.index = daily.index.tz_localize(None)
        daily.drop(["Adj Close", 'Volume'], axis=1, inplace=True)
        daily["pre_close"] = daily['Close'].shift(1)
        daily["pre_low"] = daily['Low'].shift(1)
        daily["pre_high"] = daily['High'].shift(1)
        daily = daily.ffill()
        daily['sig'] = daily['minema']- daily['hourema']
        return daily


    def plot(symbol):
        df = get_intra_data(symbol)

        y1 = df.loc[:, 'High'].values
        x = np.array([i for i in range(1, len(y1) + 1)])
        peaks1, _ = find_peaks(y1)
        # plt.plot(peaks1, y1[peaks1], "x")
        # y1[peaks1]

        y2 = df.loc[:, 'Low'].values * -1
        x = np.array([i for i in range(1, len(y1) + 1)])
        peaks2, _ = find_peaks(y2)
        # plt.plot(peaks2, y2[peaks2] * -1, "x")
        # y2[peaks2]*-1

        # this way the   x-axis corresponds to the index of x
        y = df.loc[:, 'Close'].values
        # plt.plot(x - 1, y)
        #
        # for x1 in x:
        #     plt.vlines(x=x1, ymin=min(y2 * -1), ymax=max(y1), colors='green', ls=':', lw=1)
        #
        # for x1 in y1[peaks1]:
        #     plt.hlines(y=x1, xmin=min(x), xmax=max(x), colors='red', ls=':', lw=1)
        #
        # for x1 in y2[peaks2] * -1:
        #     plt.hlines(y=x1, xmin=min(x), xmax=max(x), colors='green', ls=':', lw=1)

        return df,y1,y2,peaks1,peaks2




    def ref():
        global h1,l1,peaks1,peaks2,y1,y2,p
        lis1 = h1
        lis2 = l1
        for i in range(p,len(y1)):
            if i in peaks1:
                h1.append(y1[i])
                p = i+1
                if i in peaks2:
                    l1.append(y2[i]*-1)
                    p = i+1
                    break
                break
            if i in peaks2:
                l1.append(y2[i]*-1)
                p = i+1
                break

    # plt.plot(x-1, df.loc[:,'minema'])

    df,y1,y2,peaks1,peaks2 = plot(symbol)

    # df = get_intra_data('SBIN.NS')

    df.reset_index(inplace = True)


    p = 0
    pos = 0

    h1 = []
    l1 = []
    flag = 0
    percent = []
    # ref()


    for _ in range(len(y1)):
        prep = p
        ref()
        if prep == p: break
        if not(len(h1) >=2) or len(l1) == 0:
            continue

        if pos == 0 :
            if h1[-1] > h1[-2] and df.loc[p-1,"sig"]>0:
                bp = h1[-2]
                tsl = l1[-1]
                # print(f"Buyed at {bp} with TSL : {round(tsl,2)} with p value {p}")
                pos = +1
        if pos == 1 and l1[-1] != tsl and df.loc[p-1, "Datetime"].time() != dt.datetime(2020, 2, 2, 15, 15).time():
            if l1[-1] >= tsl :
                tsl = l1[-1]
                # print(f"TSL Updated to {round(tsl,2)} with p value {p}")
            else :
                per = (tsl / bp - 1) * 100
                # print(f"SL Hit at {tsl} with p value {p}  and {round(per,2)}%\n")

                percent.append(per)
                pos = 0
        if df.loc[p-1, "Datetime"].time() == dt.datetime(2020, 2, 2, 15, 15).time() and pos == 1:
            pos = 0
            tsl = df.loc[p, "Open"]
            per = (tsl / bp - 1) * 100
            # print(f"position closed at {tsl} with p value {p} and {round(per,2)}%\n")

            percent.append(per)


    p = 0
    pos = 0

    h1 = []
    l1 = []
    flag = 0
    # percent = []
    # ref()
    print(h1,l1)
    # p == len(y1)-1
    for _ in range(len(y1)):
        prep = p
        ref()
        if prep == p : break
        if not(len(l1) >=2) or len(h1) == 0:
            continue

        if pos == 0 :
            if l1[-1] < l1[-2] and df.loc[p-1,"sig"] < 0:
                sp = l1[-2]
                tsl = h1[-1]
                # print(f"Selling at {sp} with TSL : {round(tsl,2)} with p value {p}")
                pos = +1
        if pos == 1 and h1[-1] != tsl and df.loc[p-1, "Datetime"].time() != dt.datetime(2020, 2, 2, 15, 15).time():
            if h1[-1] < tsl :
                tsl = h1[-1]
                # print(f"TSL Updated to {round(tsl,2)} with p value {p}")
            else :
                per = (sp / tsl - 1) * 100
                # print(f"SL Hit at {tsl} with p value {p} and {round(per,2)}%\n")
                percent.append(per)
                pos = 0
        if df.loc[p-1, "Datetime"].time() == dt.datetime(2020, 2, 2, 15, 15).time() and pos == 1:
            pos = 0
            tsl = df.loc[p,"Open"]
            per = (sp / tsl - 1) * 100
            # print(f"position closed at {tsl} with p value {p} and {round(per,2)}%\n")

            percent.append(per)
    print(f'{symbol} : {sum(percent)}%')
    p_l.append(sum(percent))

symbols =['ADANIPORTS.NS',
     'ASIANPAINT.NS',
     'AXISBANK.NS',
     'BAJAJ-AUTO.NS',
     'BAJAJFINSV.NS',
     'BAJFINANCE.NS',
     'BHARTIARTL.NS',
     'BPCL.NS',
     'BRITANNIA.NS',
     'CIPLA.NS',
     'COALINDIA.NS',
     'DIVISLAB.NS',
     'DRREDDY.NS',
     'EICHERMOT.NS',
     'GAIL.NS',
     'GRASIM.NS',
     'HCLTECH.NS',
     'HDFC.NS',
     'HDFCBANK.NS',
     'HDFCLIFE.NS',
     'HEROMOTOCO.NS',
     'HINDALCO.NS',
     'HINDUNILVR.NS',
     'ICICIBANK.NS',
     'INDUSINDBK.NS',
     'INFY.NS',
     'IOC.NS',
     'ITC.NS',
     'JSWSTEEL.NS',
     'KOTAKBANK.NS',
     'LT.NS',
     'M&M.NS',
     'MARUTI.NS',
     'NESTLEIND.NS',
     'NTPC.NS',
     'ONGC.NS',
     'POWERGRID.NS',
     'RELIANCE.NS',
     'SBILIFE.NS',
     'SBIN.NS',
     'SUNPHARMA.NS',
     'TATAMOTORS.NS',
     'TATASTEEL.NS',
     'TCS.NS',
     'TECHM.NS',
     'TITAN.NS',
     'ULTRACEMCO.NS',
     'UPL.NS',
     'WIPRO.NS']
# final = pd.DataFrame()
# tick = []
p_l =[]
p = 0
pos = 0

y1 = []
y2 = []
h1 = []
l1 = []
flag = 0
percent = []
for symbol in symbols:
    main(symbol)
    # tick.append(symbol)
    # overall = pd.DataFrame.from_dict({"p_l": p_l}, orient='columns', dtype=None, columns=None)


# plt.plot(np.array(percent).cumsum())