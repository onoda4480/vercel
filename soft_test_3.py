from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# CSVファイルからデータの読み込み
data = pd.read_csv('date_4.csv')

# 日付と気温、湿度、売上の列を取得
dates = pd.to_datetime(data['date'], format="%Y/%m/%d", utc=True)
temperatures = data['kion']
humidities = data['situdo']
sales = data.iloc[:, 3:]
#data['4']  # 売上データの列名を適宜修正してください

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
start_date = '2022-04'
end_date = '2023-04'

# 指定した範囲の月次データを生成
future_dates = pd.date_range(start=start_date, end=end_date, freq='M').to_period('M').to_timestamp()

# 気温の予測
future_X = np.column_stack((future_dates.year, future_dates.month, future_dates.day))
forecast_temperature = model_temperature.predict(future_X)

# 湿度の予測
forecast_humidity = model_humidity.predict(future_X)

# 売上の予測
forecast_sales = model_sales.predict(future_X)

# 予測結果の表示
print("気温の予測結果:")
print(forecast_temperature)
print("湿度の予測結果:")
print(forecast_humidity)
print("売上の予測結果:")
print(forecast_sales)

#forecast_sales.reverse()
#forecast_sales_list = [forecast_sales]
#print(forecast_sales_list.reverse())
#print(forecast_sales_list)
#forecast_sales_sorted = np.sort((forecast_sales)[:-1])[::-1]

data_forecast_sales = pd.DataFrame(forecast_sales).T
print(data_forecast_sales)

print("売上の予測結果（日付付き）:")
i = 0
for i in range(data_forecast_sales.shape[1]):
    data_forecast_sales = data_forecast_sales.sort_values(by=data_forecast_sales.columns[i], ascending=False)
    print(f"売上の予測結果:"+str(i)+"")
    print(data_forecast_sales[i])
    i=+1

i = int(input())
print(data_forecast_sales[i])
#print("売上の予測結果（日付付き）:")
#print(forecast_sales_sorted)

# 予測結果の可視化
fig, ax1 = plt.subplots()

ax1.plot(dates, temperatures, label="Actual Temperature", color='red')
ax1.plot(future_dates, forecast_temperature, '-', label="Forecast Temperature", color='orange')
ax1.set_ylabel("Temperature")
ax1.tick_params(axis='y', labelcolor='red')

ax2 = ax1.twinx()
ax2.plot(dates, humidities, label="Actual Humidity", color='blue')
ax2.plot(future_dates, forecast_humidity, '-', label="Forecast Humidity", color='cyan')
ax2.set_ylabel("Humidity")
ax2.tick_params(axis='y', labelcolor='blue')

ax3 = ax1.twinx()
ax3.spines['right'].set_position(('outward', 60))
ax3.plot(dates, sales, label="Actual Sales", color='green')
ax3.plot(future_dates, forecast_sales, '-', label="Forecast Sales", color='purple')
ax3.set_ylabel("Sales")
ax3.tick_params(axis='y', labelcolor='green')

# 軸ラベルの表示
lns = ax1.get_lines() + ax2.get_lines() + ax3.get_lines()
ax1.legend(lns, [line.get_label() for line in lns], loc='upper left')

# 軸目盛りの設定
ax1.xaxis.set_major_locator(mdates.MonthLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

# グラフのタイトルと表示
plt.title("Temperature, Humidity, and Sales Forecast")
plt.show()

