import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import talib
import yfinance as yf

ADA_data = yf.download("^GSPC", start="2021-08-01", end="2021-09-15", interval="2m", auto_adjust= True)
slowk, slowd = talib.STOCH(ADA_data["High"], ADA_data["Low"], ADA_data["Close"], fastk_period=14, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
slowk = slowk.tolist()
slowd = slowd.tolist()
print(slowk)
ADA_data.insert(5, "slowk", slowk, True)
ADA_data.insert(6, "slowd", slowd, True)
print(ADA_data)
signal_list = []
check = 0
count = 0
# Setting the buy signal (Stoch under 20 and K over D) , signal_list --> 0 = pass, 1 = buy, 2 = sell.
for k in slowk:
    print(k)
    if k < 20 and k >= slowd[count] and check == 0:
        signal_list.append(1)
        check = 1
    elif k > 80 and k <= slowd[count] and check == 1:
        signal_list.append(2)
        check = 0
    else:
        signal_list.append(0)
    count += 1
print(count)
ADA_data.insert(7, "signal_list", signal_list, True)
count_2 = 0
for initial_price in signal_list:
    if initial_price == 1:
        i_price = ADA_data.iloc[count_2, 3]
        break
    count_2 += 1
count_3 = 0
total_return = 0
for signal in signal_list:
    if signal ==1:
        buy_price = ADA_data.iloc[count_3,3]
        profit = 0
    elif signal == 2:
        sell_price = ADA_data.iloc[count_3,3]
        profit = sell_price - buy_price
    else:
        profit = 0
    total_return += profit
    count_3 += 1
Yld = (total_return/i_price)*100
print(f'Total profit is: {total_return}')
print(f'Total yield is: {Yld}%')


