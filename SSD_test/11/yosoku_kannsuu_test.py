import numpy as np
import pandas as pd
from flask import Flask, render_template, request
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import json


def yosoku(dname):
#CSVファイルからデータの読み込み
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
    start_date = '2023-01'
    end_date = '2024-01'

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
    

    sales_list = []
        
    for row in sales:
        sales_list.append(row)
    data_forecast_sales = pd.DataFrame(forecast_sales.T, columns=future_dates)
    data_forecast_sales.index = sales_list
    data_forecast_sales = data_forecast_sales.iloc[:len(sales_list)]
    
#print(sales_list)
        #data_forecast_sales.index = sales_list

    #while 1:
    #    a = int(input('番号を選択してください。'))
    #    a = a -1
    #    if a < 0:
    #        print('もう一度入力してください。')
    #    else:
    #        break
    #a = 1
    #print("売上の予測結果:")
    #data_forecast_sales = data_forecast_sales.iloc[:, a] 
    #data_forecast_sales=data_forecast_sales.sort_values(ascending=False)
        # 予測結果をリスト形式に変換
    forecast_sales_list = data_forecast_sales.iloc[:, dname].tolist()
    forecast_sales_list = sorted(forecast_sales_list, reverse=True)
    
    # 予測結果をJSON形式で返す
    return forecast_sales_list
    #return data_forecast_sales.to_json()

dname = 1
print(yosoku(dname))