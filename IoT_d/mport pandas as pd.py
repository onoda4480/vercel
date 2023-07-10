import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
# energydate.csvの読み込み
dat_df = pd.read_csv('energydata.csv', sep=',')
# 確認
dat_df.head() # 先頭部の表示
#print(dat_df.shape) # 配列サイズ表示
#print(dat_df.dtypes) # 型の確認
#p8
dat_df['date'] = pd.to_datetime(dat_df['date'], format = '%Y-%m-%d %H:%M:%S')
#print(dat_df['date'].dtypes) # 型の確認
#print(type(dat_df['date'][0])) # date列の要素はTimestamp型
dat_df['dif_min'] = dat_df['date'].diff().dt.total_seconds()/60 # diffを使って1行前との差分を計算
dat_df['dif_min'] = dat_df['dif_min'].fillna(0) # 1行目が欠損値（NaN）になるため，0で補完
dat_df['dif_min'].head()
#print(dat_df['dif_min'].head())
#print(dat_df['dif_min'].describe())
#p9
dat_df['cum_min'] = dat_df['dif_min'].cumsum()
dat_df[['date', 'cum_min']].head()
dat_df['cum_hour'] = (dat_df['cum_min']/60).round(2).astype(int) # 小数点第2位で四捨五入して，整数化する
dat_df[['date', 'cum_min', 'cum_hour']].head(10)
#print(dat_df[['date', 'cum_min', 'cum_hour']].head(30))
#p10
#print(dat_df.isnull().sum(axis=1).sort_values(ascending=False))
#print(dat_df.isnull().sum(axis=0))
dat_df.describe()
dat_df.groupby('cum_hour').mean() # groupbyを使って，cum_hourを集計キーとし，各項目の平均を算出
dat_df.groupby('cum_hour').std() # 同様に，標準偏差を算出
#print(dat_df.groupby('cum_hour').mean(numeric_only=True))
#print(dat_df.groupby('cum_hour').std())
'''
#p11
plt.plot(dat_df['cum_min'], dat_df['Appliances'])
plt.xlabel('cum_min')
plt.ylabel('Appliances')
plt.show()
#p12
plt.plot(dat_df['cum_min'], dat_df['T1'], 'r-', label='T1')
plt.plot(dat_df['cum_min'], dat_df['T2'], 'g-', label='T2')
plt.plot(dat_df['cum_min'], dat_df['T3'], 'b-', label='T3')
plt.xlabel('cum_min')
plt.legend()
plt.show()
'''
#p13
#print(dat_df[8585:8588])
dat_df[8585:8588].fillna(method='ffill') # Forward-Fill
##dat_df[8585:8588].interpolate() # エラー
dat_tmp_df = dat_df
dat_tmp_df['T3'] = dat_df['T3'].interpolate()
dat_tmp_df[8585:8588]
#print(dat_tmp_df[8585:8588])
#p14
dat_df['cum_6hour'] = (dat_df['cum_min']/360).round(2).astype(int)
# 確認
#print(dat_df['cum_6hour'].unique())
#print(dat_df[['date', 'cum_min', 'cum_6hour']].head(60))
#p15
dat_df = dat_df.drop(['date', 'dif_min', 'cum_min'], axis=1)
dat_df_mean = dat_df.groupby('cum_6hour').mean()
dat_df_std = dat_df.groupby('cum_6hour').std()
#print(dat_df_mean)
#print(dat_df_std)
#p16
dat_features = pd.merge(dat_df_mean, dat_df_std, left_index=True, right_index=True)
#print(dat_features.head())
#print(dat_features.shape)
dat_features.head()
event_df = pd.read_csv('event.csv', sep=',')
event_df.head() # 先頭部の表示
event_df['date'] = pd.to_datetime(event_df['date'], format = '%Y-%m-%d %H:%M:%S')
base_time = '2016-01-11 17:00:00'
event_df['dif_min'] = event_df['date'] - dt.datetime.strptime(base_time, '%Y-%m-%d %H:%M:%S')
event_df['dif_min'] = event_df['dif_min'].dt.total_seconds()/60
event_df['cum_6hour'] = (event_df['dif_min']/360).round(2).astype(int)
event_df['event'] = 1
event_df = event_df[['cum_6hour','event']]
event_df = event_df[~event_df.duplicated()]
event_df = event_df.set_index(['cum_6hour'])
#print(event_df)
dat_event = dat_features.join(event_df, how='left')
dat_event = dat_event.fillna(0)
tmp = dat_df[dat_df['cum_6hour'] == 0]
tmp = tmp.drop(['cum_6hour'], axis=1)
tmp = tmp.rolling(6).mean()
tmp = tmp.dropna()
print(tmp.shape)
#print(tmp)
#print(dat_event)
hid = dat_df['cum_6hour'].unique()
dat_slide_features = []
for i in range(len(hid)):
    tmp = dat_df[dat_df['cum_6hour'] == i]
    tmp = tmp.drop(['cum_6hour'],axis = 1)
    tmp_mean = tmp.rolling(6).mean()
    tmp_mean = tmp_mean.dropna()
    tmp_std = tmp.rolling(6).std()
    tmp_std = tmp_std.dropna()
    tmp2 = (np.array(tmp_mean['Appliances']).tolist() + np.array(tmp_mean['lights']).tolist() +
    np.array(tmp_mean['T1']).tolist() + np.array(tmp_mean['RH_1']).tolist() +
    np.array(tmp_mean['T2']).tolist() + np.array(tmp_mean['RH_2']).tolist() +
    np.array(tmp_mean['T3']).tolist() + np.array(tmp_mean['RH_3']).tolist() +
    np.array(tmp_mean['T4']).tolist() + np.array(tmp_mean['RH_4']).tolist() +
    np.array(tmp_mean['T5']).tolist() + np.array(tmp_mean['RH_5']).tolist() +
    np.array(tmp_std['Appliances']).tolist() + np.array(tmp_std['lights']).tolist() +
    np.array(tmp_std['T1']).tolist() + np.array(tmp_std['RH_1']).tolist() +
    np.array(tmp_std['T2']).tolist() + np.array(tmp_std['RH_2']).tolist() +
    np.array(tmp_std['T3']).tolist() + np.array(tmp_std['RH_3']).tolist() +
    np.array(tmp_std['T4']).tolist() + np.array(tmp_std['RH_4']).tolist() +
    np.array(tmp_std['T5']).tolist() + np.array(tmp_std['RH_5']).tolist())
    dat_slide_features.append(tmp2)
dat_slide_features = pd.DataFrame(dat_slide_features)
print(dat_slide_features.shape) # → （484, 744）
print(dat_slide_features.head())
tmp3 = dat_event[['event']]
dat_event2 = pd.concat([dat_slide_features, tmp3], axis=1)
print(dat_event2.shape) # → (484, 745)
print(dat_event2.head())

dat_df = pd.read_csv('energydata.csv', sep=',')[['date', 'Appliances']]
dat_df['date'] = pd.to_datetime(dat_df['date'], format='%Y-%m-%d %H:%M:%S')
dat_df.head()
plt.plot(dat_df['date'], dat_df['Appliances'])
plt.xlabel('date')
plt.xticks(rotation=30)
plt.ylabel('Appliances')
plt.show()

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

import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
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
verbose=1, epochs=500, validation_split=0.2)
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