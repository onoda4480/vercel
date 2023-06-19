from sklearn.svm import SVR
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# CSVファイルからデータの読み込み
data = pd.read_csv("date_1.csv")

# 日付と気温の列を取得
dates = data['date']
temperatures = data['kion']

# 日付データを数値に変換
X = np.arange(len(dates)).reshape(-1, 1)

# モデルの構築と学習
model = SVR(kernel='rbf', C=100, gamma=0.1)
model.fit(X, temperatures)

# 将来の日付の生成
future_dates = np.arange(len(dates), len(dates) + 7).reshape(-1, 1)

# 気温の予測
forecast = model.predict(future_dates)

# 予測結果の表示
print("予測結果:")
print(forecast)

# 予測結果の可視化
plt.plot(dates, temperatures, label="Actual")
plt.plot(future_dates, forecast, label="Forecast")
plt.xlabel("Date")
plt.legend()
plt.show()