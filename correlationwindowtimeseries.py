import numpy as np
import pandas as pd
from matplotlib import pyplot
import matplotlib.ticker as mtick

coinlist = sorted(["ETHUSDT","BTCUSDT","ADAUSDT","DOTUSDT"])  # two is min
number = 1032 
windowsize = 168 
series2 = pd.DataFrame(data=None)
for coin in coinlist:
    series1 = pd.DataFrame(data=None)
    try:
        series1[list({"date",coin})] = pd.read_csv("https://www.cryptodatadownload.com/cdd/Binance_" + coin + "_1h.csv",skiprows = 1)[list({"date","close"})][:number]
        print(series1.head())  # some webesite on the inernet, only educational purposes only
    except:
        print("some issues with: ", coin)
        pass
    if series2.empty:
        series2 = series1 
    else:    
        series2 = pd.merge(series1, series2, how = "inner", on="date")

series2["date"] = pd.to_datetime(series2["date"]) 
series2[(coinlist)]  = series2[(coinlist)].pct_change(1)  
print(series2.head())

koreltable = series2
print("total coins: ", len(coinlist))
pairlist = []
for iter1 in range(0, len(coinlist)):
    for iter2 in range(0, iter1):
             pairlist.append((coinlist[iter1], coinlist[iter2]))

for x in pairlist:
    print(x)
pairlist = sorted(pairlist)
print("total pairs: ", len(pairlist))

korel =[]
korelname =[]
for tt in range(len(pairlist)):
    korel.append([])
    korelname.append([])
    for window in koreltable.loc[:,pairlist[tt]].rolling(window=windowsize, min_periods=windowsize):
        korelname[tt] = pairlist[tt]
        if len(window) == windowsize:
            korel[tt].append(window.corr().iloc[0,1])
  
ax = []
pyplot.figure(figsize=(12, 18), dpi = 90)  
ax.append(pyplot.subplot(7,1,1))  

for coin in coinlist:
    ax[0].plot(koreltable["date"].iloc[windowsize:],koreltable[coin].iloc[windowsize:], c=np.random.rand(3,), lw =  1)
    ax[0].set_title("Hourly returns on " + str(" and ".join(coinlist )) + " in USDT" ,fontsize=14)

fmt = '%.2f%%' 
xticks = mtick.FormatStrFormatter(fmt)
ax[0].yaxis.set_major_formatter(xticks)
ax[0].legend(coinlist)
ax[0].axhline(y=0, color='k', linestyle='-', linewidth=0.5)

for tt in range(1,(len(pairlist)+1),1):
    ax.append(pyplot.subplot((int(1.5+len(pairlist)/2)),2,tt+2))
    ax[tt].plot(koreltable["date"].iloc[(windowsize-1):],korel[tt-1], c=np.random.rand(3,), lw =  1.5)
    ax[tt].set_title("Correlation between " + str(" and ".join(korelname[tt-1])) + " window length: " + str(windowsize),fontsize=10)
    pyplot.xticks(fontsize=7)

pyplot.subplots_adjust(left=0.1, bottom=0.1,  right=0.9, top=0.9,   wspace=0.1,  hspace=0.4)
pyplot.show() 
