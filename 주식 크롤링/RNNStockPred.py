# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 16:22:46 2022

@author: seon
"""
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
import numpy as np
import matplotlib.pyplot as plt
import Analyzer

mk = Analyzer.MarketDB()
raw_df = mk.get_daily_price('005930','2021-01-01','2022-11-07')
print(raw_df)
     
window_size = 10
data_size = 5
# 최솟값과 최댓값을 이용하여 0 ~ 1 값으로 변환
def MinMaxScaler(data):
    numerator = data - np.min(data, 0)
    denominator = np.max(data, 0) - np.min(data, 0)
    # 0으로 나누기 에러가 발생하지 않도록 매우 작은 값(1e-7)을 더해서 나눔
    return numerator / (denominator + 1e-7)
dfx = raw_df[['open','high','low','volume', 'close']]
dfx = MinMaxScaler(dfx)
dfy = dfx[['close']]

x = dfx.values.tolist()
y = dfy.values.tolist()

data_x = []
data_y = []

for i in range(len(y)-window_size):
    _x = x[i : i + window_size]
    _y = y[i+window_size]   # 다음날 종가
    data_x.append(_x)
    data_y.append(_y)
    # print(_x, '->',_y)
    # print('==========')
    
train_size = int(len(data_y) * 0.7)
train_x = np.array(data_x[0 : train_size])
train_y = np.array(data_y[0 : train_size])

test_size = len(data_y) - train_size
test_x = np.array(data_x[train_size : len(data_x)])
test_y = np.array(data_y[train_size : len(data_y)])

model = Sequential()
# output을 시퀀스의 마지막 값이 아닌 전체 시퀀스로 반환
model.add(LSTM(units=10, activation='relu', return_sequences=True, input_shape=(window_size, data_size)))
model.add(Dropout(0.1))
model.add(LSTM(units=10, activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(units=1))
model.summary()