import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense

dat_df = pd.read_csv('date_6.csv', sep=',')[['date', 'kion']]
dat_df['date'] = pd.to_datetime(dat_df['date'], format='%Y-%m-%d %H:%M:%S')
train = dat_df[dat_df['date'] < '2016-04-11 17:00:00'] # 訓練用，テスト用に75:25でデータを分ける
test = dat_df[dat_df['date'] >= '2016-04-11 17:00:00']
from sklearn.preprocessing import MinMaxScaler # [0,1]に正規化する
mc = MinMaxScaler()
train = mc.fit_transform(train[['kion']])
test = mc.fit_transform(test[['kion']])
width = 6 # スライド窓幅=144．10分ごとにデータがあるので 6個×24時間=144
train = train.flatten()
train_vec = []
for i in range(len(train)-width):
    train_vec.append(train[i:i+width])
test = test.flatten()
test_vec = []
for i in range(len(test)-width):
    test_vec.append(test[i:i+width])
    

train_vec = np.array(train_vec)
test_vec = np.array(test_vec)

model = Sequential() # シーケンシャルモデルの作成
model.add(Dense(128, activation='relu', input_shape=(144,))) # 特徴量 144=スライド窓幅
model.add(Dense(64, activation='relu')) # Denseで中間層作成
model.add(Dense(32, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(128, activation='relu'))
model.add(Dense(144, activation='sigmoid')) # 出力ノード数は入力と同じ144．活性化関数はシグモイド
model.summary() # 出力サイズとパラーメータの表示
model.compile(loss='mse', optimizer='adam') # 学習条件のセット．誤差関数は平均事情誤差（mse），最適化関数はAdam法
hist = model.fit(train_vec, train_vec, batch_size=128,
verbose=1, epochs=50, validation_split=0.2)
# 説明関数＝目的関数＝train_vec， ミニバッチ数＝128， エポック数 20， 訓練データの内検証データとして使うのは20%
plt.plot(hist.history['loss'], label='loss')
plt.plot(hist.history['val_loss'], label='val_loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend()
plt.show() # エポック数ごとの誤差

pred = model.predict(test_vec)
# 作成したモデルにテストデータ（test_vec）を入れ， 予測値を得る（pred）
plt.plot(test_vec[:,0], label='test')
plt.plot(pred[:,0], label='pred')
plt.legend()
plt.show() 