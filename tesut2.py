import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Excelファイルから売上データを読み込む
sales_df = pd.read_excel("SSD_04_Data_0.xlsx", sheet_name="売上")

# Excelファイルから温湿度データを読み込む
weather_df = pd.read_excel("SSD_04_Data_0.xlsx", sheet_name="温湿度",index_col=0)
#print(sales_df.head())
#print(weather_df.head())

#i = sales_df.iloc[:,:0]
#sales_df= sales_df.drop(['ID'],axis=1)
#weather_df = weather_df.drop(['年月'])
weather_df = weather_df.transpose()
print(sales_df.head())
#sales_df = sales_df.transpose()
# 売上データと温湿度データを結合する
data_df = pd.concat([sales_df, weather_df], axis=1)
print(data_df.head())
data_df.to_csv('output2.csv', index=False)