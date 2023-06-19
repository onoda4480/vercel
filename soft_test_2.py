from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# CSVファイルからデータの読み込み
data = pd.read_csv('date_4.csv', encoding='shift-jis')

# 日付と気温、湿度、売上の列を取得
dates = pd.to_datetime(data['date'], format="%Y/%m/%d", utc=True)
temperatures = data['kion']
humidities = data['situdo']
num_sales = 50  # 売上データの数を指定してください

# 日付データを年、月、日に分割して特徴量として追加
data['date'] = dates
data['year'] = dates.dt.year
data['month'] = dates.dt.month
data['day'] = dates.dt.day

# 特徴量と目標変数の列を取得
X = data[['year', 'month', 'day']].values
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

# 予測する日付の範囲を指定
start_date = '2023-05-01'
end_date = '2023-07-31'

# 指定した範囲の日次データを生成
future_dates = pd.date_range(start=start_date, end=end_date, freq='D').to_period('D').to_timestamp()

# 予測する特徴量を作成
future_X = np.column_stack((future_dates.year, future_dates.month, future_dates.day))

# 気温の予測
forecast_temperature = model_temperature.predict(future_X)

# 湿度の予測
forecast_humidity = model_humidity.predict(future_X)

# 売上の予測
forecast_sales = np.zeros((len(future_dates), num_sales))
for i, model in enumerate(model_sales):
    forecast_sales[:, i] = model.predict(future_X)

# 売上データ別の予測結果を計算
forecast_sales_sum = np.sum(forecast_sales, axis=0)

# 予測結果をデータ別にソート
sorted_indices = np.argsort(forecast_sales_sum)[::-1]
sorted_sales_names = [sales_names[i] for i in sorted_indices]
sorted_forecast_sales_sum = forecast_sales_sum[sorted_indices]

# データ別の予測結果と順位を表示
print("予測結果の順位:")
for i, (name, sales) in enumerate(zip(sorted_sales_names, sorted_forecast_sales_sum), 1):
    print(f"{i} {name} {sales}")

# 予測結果をデータ別に順位付け
sorted_indices = np.argsort(sorted_forecast_sales_sum)[::-1]
sorted_sales_names = [sorted_sales_names[i] for i in sorted_indices]
sorted_forecast_sales_sum = sorted_forecast_sales_sum[sorted_indices]

# 予測結果の日付データと売上データを作成
forecast_dates_sorted = future_dates[sorted_indices]
forecast_data = pd.DataFrame({'Date': forecast_dates_sorted, 'Sales': sorted_forecast_sales_sum})

# データ別の予測結果と順位を表示
print("予測結果の順位:")
for i, (date, name, sales) in enumerate(zip(forecast_data['Date'], sorted_sales_names, forecast_data['Sales']), 1):
    print(f"{date.strftime('%Y-%m-%d')} {i} {name} {sales}")

forecast_sales_max = np.max(forecast_sales, axis=1)

# 予測結果の日付データと売上データを作成
forecast_dates_sorted = future_dates[sorted_indices]
forecast_sales_sorted = forecast_sales_max[sorted_indices]

# 予測結果のDataFrameを作成
sorted_forecast_data = pd.DataFrame({'Date': forecast_dates_sorted, 'Sales': forecast_sales_sorted})

# 年と月を抽出
sorted_forecast_data['Year'] = sorted_forecast_data['Date'].dt.year
sorted_forecast_data['Month'] = sorted_forecast_data['Date'].dt.month

# 月ごとにグループ化してソート
sorted_forecast_data = sorted_forecast_data.groupby(['Year', 'Month']).apply(lambda x: x.sort_values('Sales', ascending=False)).reset_index(drop=True)

# 予測結果の表示
print(sorted_forecast_data)


# 月ごとの売上データと商品名の表示
def display_sales_rank(month, forecast_data, sales_names):
    # 指定した月の売上データを抽出
    monthly_sales = forecast_data[forecast_data['Month'] == month]

    # 売上の降順でソート
    sorted_sales = monthly_sales.sort_values('Sales', ascending=False).reset_index(drop=True)

    print(f"{sorted_sales['Year'].values[0]}年 {month}月の売上順位:")

    # 売上順位と商品名・売上金額の表示
    for i, row in sorted_sales.iterrows():
        print(f"{i+1}位 {sales_names[i]} {int(row['Sales'])}円")

# 予測結果の日付データから年と月を抽出
forecast_data['Year'] = forecast_data['Date'].dt.year
forecast_data['Month'] = forecast_data['Date'].dt.month

# 4月の売上順位を表示
display_sales_rank(4, forecast_data, sales_names)
