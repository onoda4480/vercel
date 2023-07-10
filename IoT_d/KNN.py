import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
dat_df = pd.read_csv('energydata.csv', sep=',')[['date', 'Appliances']]
dat_df['date'] = pd.to_datetime(dat_df['date'], format='%Y-%m-%d %H:%M:%S')

train = dat_df[dat_df['date'] < '2016-04-11 17:00:00'] # 訓練用，テスト用に75:25でデータを分ける
test = dat_df[dat_df['date'] >= '2016-04-11 17:00:00']
from sklearn.preprocessing import MinMaxScaler # [0,1]に正規化する
mc = MinMaxScaler()
train = mc.fit_transform(train[['Appliances']])
test = mc.fit_transform(test[['Appliances']])
width = 144 # スライド窓幅=144．10分ごとにデータがあるので 6個×24時間=144
train = train.flatten()
train_vec = []
for i in range(len(train)-width):
    train_vec.append(train[i:i+width])
test = test.flatten()
test_vec = []
for i in range(len(test)-width):
    test_vec.append(test[i:i+width])

from sklearn.neighbors import NearestNeighbors #
train_vec = np.array(train_vec)
test_vec = np.array(test_vec)
model = NearestNeighbors(n_neighbors=1) # k=1 のk-NN
model.fit(train_vec)
dist, _ = model.kneighbors(test_vec)
dist = dist / np.max(dist) # 最大値で割って正規化する
plt.plot(dist)
plt.show()
