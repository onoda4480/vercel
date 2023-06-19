from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# CSVファイルからデータの読み込み
data = pd.read_csv('date_1.csv', encoding='shift-jis')

# 日付と気温、湿度、売上の列を取得
dates = pd.to_datetime(data['date'], format="%Y/%m/%d", utc=True)
temperatures = data['kion']
humidities = data['situdo']
num_sales = 50  # 売上データの数を指定してください


# 売上データの列数を取得
#num_sales = data.shape[1] - 4  # 日付と気温、湿度の列を除いた列数を計算

# 日付データを年と月に分割して特徴量として追加
data['date'] = dates
data['year'] = dates.dt.year
data['month'] = dates.dt.month

# 特徴量と目標変数の列を取得
X = data[['year', 'month']].values
y_temperature = temperatures.values
y_humidity = humidities.values
y_sales = data.iloc[:, 4:4+num_sales].values  # 売上データの列位置を適宜修正してください

# モデルの構築と学習
model_temperature = RandomForestRegressor(n_estimators=100, random_state=42)
model_temperature.fit(X, y_temperature)

model_humidity = RandomForestRegressor(n_estimators=100, random_state=42)
model_humidity.fit(X, y_humidity)

model_sales = []
sales_names = ['syouhinmei']  # 売上データの名前を保持するリスト
for i in range(num_sales):
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y_sales[:, i])
    model_sales.append(model)
    sales_names.append(data.columns[4+i])  # 売上データの列名を保持

# 予測する月の範囲を指定
start_date = '2016-04'
end_date = '2017-03'

# 指定した範囲の月次データを生成
future_dates = pd.date_range(start=start_date, end=end_date, freq='M').to_period('M').to_timestamp()

# 気温の予測
future_X = np.column_stack((future_dates.year, future_dates.month))
forecast_temperature = model_temperature.predict(future_X)

# 湿度の予測
forecast_humidity = model_humidity.predict(future_X)

# 売上の予測
forecast_sales = np.zeros((len(future_dates), num_sales))
for i, model in enumerate(model_sales):
    forecast_sales[:, i] = model.predict(future_X)

# 予測結果の表示
print("気温の予測結果:")
print(forecast_temperature)
print("湿度の予測結果:")
print(forecast_humidity)
print("売上の予測結果:")
print(forecast_sales)

#print(forecast_sales.shape)

# 売上予測結果の計算
forecast_sales_max = np.max(forecast_sales, axis=1)

# 予測結果の昇順に並び替え
sorted_indices = np.argsort(forecast_sales_max)[::-1]
sorted_forecast_sales = forecast_sales_max[sorted_indices]

# 予測結果の日付データと売上データを作成
forecast_dates_sorted = future_dates[sorted_indices]
forecast_data = pd.DataFrame({'Date': forecast_dates_sorted, 'Sales': sorted_forecast_sales})

# 予測結果の表示
print(forecast_data)

# 予測結果の日付データから年と月を抽出
forecast_data['Year'] = forecast_data['Date'].dt.year
forecast_data['Month'] = forecast_data['Date'].dt.month

# 年と月でソート
sorted_forecast_data = forecast_data.sort_values(['Year', 'Month'])

# ソートされた売上データの表示
print(sorted_forecast_data)


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

for i in range(num_sales):
    ax3.plot(dates, y_sales[:, i], label=f"Actual {sales_names[i]}", color='green')
    ax3.plot(future_dates, forecast_sales[:, i], '-', label=f"Forecast {sales_names[i]}", color='purple')

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
