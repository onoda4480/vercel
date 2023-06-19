import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Excelファイルから売上データを読み込む
sales_df = pd.read_excel("SSD_04_Data_0.xlsx", sheet_name="売上")

# Excelファイルから温湿度データを読み込む
weather_df = pd.read_excel("SSD_04_Data_0.xlsx", sheet_name="温湿度", index_col=0)
print(sales_df.head())
print(weather_df.head())

sales_df= sales_df.drop(0)
#weather_df = weather_df.transpose()
print()
sales_df = sales_df.transpose()
# 売上データと温湿度データを結合する
data_df = pd.concat([sales_df, weather_df], axis=1)
print(data_df.head())

#print(data_df.head())
#print(data_df.shape) # CSVの行数，列数
#print(data_df.dtypes) # 各列の型
#print(data_df.isnull().any(axis=1)) # 各行の欠損の有無
#print(data_df.isnull().any(axis=0)) # 各列の欠損の有無
#print(data_df.isnull().sum(axis=1)) # 各行の欠損の数
#print(data_df.isnull().sum(axis=0)) # 各列の欠損の数
#print(data_df.isnull().sum(axis=1))
date_df = data_df.fillna({'contact':'unknown'})
#data_df.to_excel('output.xlsx', index=False)

# データをトレーニングセットとテストセットに分割する
train_data = data_df.loc[:,0:]
test_data = data_df.loc[:,0:]

# ARIMAモデルを構築する
model = sm.tsa.statespace.SARIMAX(train_data['1'],axis=1, 
                                  order=(1, 1, 1), 
                                  seasonal_order=(0, 1, 1, 12), 
                                  exog=train_data[["平均気温(℃)", "平均湿度(％)"]],
                                  enforce_stationarity=False, 
                                  enforce_invertibility=False)

# モデルをトレーニングする
results = model.fit()
# 2023年7月の予測を作成する
forecast = results.get_prediction(start=pd.to_datetime("2023-07-01"), 
                                   end=pd.to_datetime("2023-07-31"), 
                                   exog=test_data[["temperature", "humidity"]])

# 予測値と95％信頼区間を取得する
forecast_mean = forecast.predicted_mean
forecast_ci = forecast.conf_int()

# 温湿度データを読み込み
weather_df = pd.read_excel('weather_data.xlsx', index_col=0)

# 日時列のフォーマットを変更
weather_df.index = pd.to_datetime(weather_df.index, format="%Y/%m")

# 売上データと温湿度データを結合
merged_df = pd.merge(sales_df, weather_df, left_index=True, right_index=True)

# ARIMAモデルの構築と予測
from statsmodels.tsa.arima.model import ARIMA

# 製品ごとに予測を行う
for product in merged_df.columns[:-2]:
    # モデルの構築
    model = ARIMA(merged_df[product], order=(1,1,1))
    results = model.fit()
    
    # 2023/7の売上予測
    forecast = results.forecast(steps=1)[0]
    print(f"{product}の2023/7の売上予測:{forecast:.0f}")




