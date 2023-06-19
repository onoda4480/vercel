import pandas as pd
import datetime as dt

# energydata.csvの読み込み
dat_df = pd.read_csv('IoT_DP\energydata.csv', sep=',')

#[型の変換，時刻の変換]
#日付がobject型になっているので扱いやすいdatatime型に変換する
dat_df['date'] = pd.to_datetime(dat_df['date'], format='%Y-%m-%d %H:%M:%S')

#時刻ではなく，開始時刻からの経過時間（分）を用意する
dat_df['dif_min'] = dat_df['date'].diff().dt.total_seconds() / 60
dat_df['dif_min'] = dat_df['dif_min'].fillna(0)

#時刻の変換
dat_df['cum_min'] = dat_df['dif_min'].cumsum()
dat_df['cum_hour'] = (dat_df['cum_min'] / 60).round(2).astype(int)

print(dat_df[['date', 'cum_min', 'cum_hour']].head(10))

#欠損値の確認，統計量の確認
print(dat_df.isnull().sum(axis=1).sort_values(ascending=False))
print(dat_df.isnull().sum(axis=0))
dat_df.describe()

dat_df.groupby('cum_hour').mean()
dat_df.groupby('cum_hour').std()

#データの可視化
import matplotlib.pyplot as plt
plt.plot(dat_df['cum_min'], dat_df['Appliances'])
plt.xlabel('cum_min')
plt.ylabel('Appliances')
#plt.show()

#台所の温度（T1)，リビングの温度（T2），洗濯室の温度（T3）を1枚の折れ線グラフ
plt.plot(dat_df['cum_min'], dat_df['T1'], 'r-', label='T1')
plt.plot(dat_df['cum_min'], dat_df['T2'], 'g-', label='T2')
plt.plot(dat_df['cum_min'], dat_df['T3'], 'b-', label='T3')
plt.xlabel('cum_min')
plt.legend()
#plt.show()

#欠損値の補完
#直前の値で補完
print(dat_df.isnull().sum(axis=1).sort_values(ascending=False))
print(dat_df[8585:8588])
print(dat_df[8585:8588].fillna(method='ffill')) # Forward-Fill

#前後の値から補完
dat_df[8585:8588].interpolate() # エラー
dat_tmp_df = dat_df
dat_tmp_df['T3'] = dat_df['T3'].interpolate()
print(dat_tmp_df[8585:8588])

#時間軸の作成
dat_df['cum_6hour'] = (dat_df['cum_min'] / 360)
print(dat_df['cum_6hour'].unique())
print(dat_df[['date','cum_min','cum_6hour']].head(50))

#特徴量の作成
dat_df = dat_df.drop(['date', 'dif_min', 'cum_min'], axis=1)
dat_df_mean = dat_df.groupby('cum_6hour').mean()
print(dat_df_mean)

#標準偏差
dat_df_std = dat_df.groupby('cum_6hour').std()
print(dat_df_std)

#特徴量の作成
dat_features = pd.merge(dat_df_mean, dat_df_std, left_index=True, right_index=True)
print(dat_features.shape)
print(dat_features.head())

#目的変数の作成
event_df = pd.read_csv('IoT_DP\event.csv', sep=',')
#print(event_df.head())

event_df['date'] = pd.to_datetime(event_df['date'], format='%Y-%m-%d %H:%M:%S')
base_time = '2016-01-11 17:00:00'
event_df['dif_min'] = event_df['date'] - dt.datetime.strptime(base_time,'%Y-%m-%d %H:%M:%S')
event_df['dif_min'] = event_df['dif_min'].dt.total_seconds()/60
event_df['cum_6hour'] = (event_df['dif_min']/360).round(2).astype(int)
event_df['event'] = 1
print(event_df)
event_df = event_df[['cum_6hour','event']]
print(event_df)
event_df = event_df[~event_df.duplicated()]
print(event_df)
event_df = event_df.set_index(['cum_6hour'])
print(event_df)

#説明変数と目的変数の結合
dat_event = dat_features.join(event_df,how='left')
print(dat_event)

dat_event = dat_event.fillna(0)
print(dat_event)

#特徴量の作成　その２

print(dat_df.head())

tmp = dat_df[dat_df['cum_6hour'] == 0]
print(tmp.head())
tmp = tmp.drop(['cum_6hour'], axis=1)
print(tmp.head())
tmp = tmp.rolling(6).mean()
print(tmp.head())
tmp = tmp.dropna()

print(tmp.shape)








# 確認
#print(dat_df.head()) # 先頭部の表示
#print(dat_df.shape) # 配列サイズ表示
#print(dat_df.dtypes) # 型の確

# 確認
#print(dat_df.head()) # 先頭部の表示
#print(event_df.shape) # 配列サイズ表示
#print(event_df.dtypes) # 型の確