from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# CSVファイルからデータの読み込み
data = pd.read_csv('date_5.csv' )

#欠損地の除去
data = data.dropna()
#print(data.head())

# 日付と気温、湿度、売上の列を取得
dates = pd.to_datetime(data['date'], format="%Y/%m/%d", utc=True)
temperatures = data['kion']
humidities = data['situdo']
sales = data.iloc[:, 3:]
#print(sales)

# 日付データを年と月に分割して特徴量として追加
data['date'] = dates
data['year'] = dates.dt.year
data['month'] = dates.dt.month
data['day'] = dates.dt.day

# 特徴量と目標変数の列を取得
X = data[['year', 'month', 'day']].values
y_temperature = temperatures.values
y_humidity = humidities.values
y_sales = sales.values

# モデルの構築と学習
model_temperature = RandomForestRegressor(n_estimators=100, random_state=42)
model_temperature.fit(X, y_temperature)

model_humidity = RandomForestRegressor(n_estimators=100, random_state=42)
model_humidity.fit(X, y_humidity)

model_sales = RandomForestRegressor(n_estimators=100, random_state=42)
model_sales.fit(X, y_sales)

# 予測する月の範囲を指定
start_date = '2023-07'
end_date = '2024-07'

# 指定した範囲の月次データを生成
future_dates = pd.date_range(start=start_date, end=end_date, freq='M').to_period('M').to_timestamp()
#print(future_dates)
#print(future_dates[1])

# 気温の予測
future_X = np.column_stack((future_dates.year, future_dates.month, future_dates.day))
forecast_temperature = model_temperature.predict(future_X)


# 湿度の予測
forecast_humidity = model_humidity.predict(future_X)

# 売上の予測
forecast_sales = model_sales.predict(future_X)

# 予測結果の表示
#print("気温の予測結果:")
#print(forecast_temperature)
#print("湿度の予測結果:")
#print(forecast_humidity)
#print("売上の予測結果:")
#print(forecast_sales)

data_forecast_sales = pd.DataFrame(forecast_sales.T, columns=future_dates)
#print(data_forecast_sales)
data_forecast_sales.info()
print(data_forecast_sales.index)

sales_list = []
for row in sales:
    sales_list.append(row)
#print(sales_list)
data_forecast_sales.index = sales_list


a = int(input('番号を選択してください。'))

print("売上の予測結果:")
data_forecast_sales = data_forecast_sales.iloc[:, a] 
data_forecast_sales=data_forecast_sales.sort_values(ascending=False)
print(data_forecast_sales.name)
data = data_forecast_sales.sort_values(ascending=False)
data['ranke'] = data.rank(ascending=False, method='min')
#print(data['ranke'])
print(data)
#print(data_forecast_sales.columns)

# 予測結果の可視化
fig, ax1 = plt.subplots()

#ax1.plot(dates, temperatures, label="Actual Temperature", color='red')
#ax1.plot(future_dates, forecast_temperature, '-', label="Forecast Temperature", color='orange')
ax1.set_ylabel("Temperature")
ax1.tick_params(axis='y', labelcolor='red')


ax2 = ax1.twinx()
#ax2.plot(dates, humidities, label="Actual Humidity", color='blue')
#ax2.plot(future_dates, forecast_humidity, '-', label="Forecast Humidity", color='cyan')
ax2.set_ylabel("Humidity")
ax2.tick_params(axis='y', labelcolor='blue')

ax3 = ax1.twinx()
ax3.spines['right'].set_position(('outward', 60))
ax3.plot(dates, sales, label="Actual Sales", color='green')
#ax3.plot(future_dates, data, '-', label="Forecast Sales", color='purple')
ax3.set_ylabel("Sales")
ax3.tick_params(axis='y', labelcolor='green')

# 軸ラベルの表示
lns = ax1.get_lines() + ax2.get_lines() + ax3.get_lines()
ax1.legend(lns, [line.get_label() for line in lns], loc='upper left')

# 軸目盛りの設定
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

# グラフのタイトルと表示
#plt.title("Temperature, Humidity, and Sales Forecast")
#plt.show()


# グラフの領域を作成
fig, ax = plt.subplots()
plt.rcParams['font.family'] = 'Meiryo'# 使用するフォントを指定

x = sales_list
height = data[50]
# 棒グラフを作成
ax.bar(x, height)

# グラフの装飾
ax.set_title("sales Bar Graph")
ax.set_xlabel("X Label")
ax.set_ylabel("Y Label")
ax.legend(["sales"])

# グラフを表示
plt.show()