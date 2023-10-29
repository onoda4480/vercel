import numpy as np
import pandas as pd
from flask import Flask, render_template, request
#from sklearn.decomposition import PCA
#from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
import cv2


app = Flask(__name__)

csv_file = 'year..csv'
df = pd.read_csv(csv_file, usecols=[0])
items = df['月'].to_list()

@app.route("/")
def show_toppage():
    return render_template('index.html', items=items)

def yosoku(dname):
#CSVファイルからデータの読み込み
    data = pd.read_csv('date_5.csv' )

#欠損地の除去
    data = data.dropna()

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
    end_date = '2024-02'

# 指定した範囲の月次データを生成
    future_dates = pd.date_range(start=start_date, end=end_date, freq='M').to_period('M').to_timestamp()
	

# 気温の予測
    future_X = np.column_stack((future_dates.year, future_dates.month, future_dates.day))
    forecast_temperature = model_temperature.predict(future_X)


# 湿度の予測
    forecast_humidity = model_humidity.predict(future_X)

# 売上の予測
    forecast_sales = model_sales.predict(future_X)

    sales_list = []
    sales_name = []

    for row in sales:
        sales_list.append(row)

    for row in csv.reader(sales):
        sales_name.append(row[0])

    data_forecast_sales = pd.DataFrame(forecast_sales.T, columns=future_dates)
    data_forecast_sales.index = sales_list
    data_forecast_sales = data_forecast_sales.iloc[:len(sales_list)]
    for i in range(50):
        data_forecast_sales.rename(index={i: sales_name[i]}, inplace=True)

    forecast_sales_list = data_forecast_sales.iloc[:, dname].tolist()
    forecast_sales_list = sorted(forecast_sales_list, reverse=True)

    # 順位と名前のDataFrameを作成
    rank_df = pd.DataFrame({'順位': range(1, len(forecast_sales_list) + 1), '名前': sales_name})

    # 予測結果を含むDataFrameを作成
    result = pd.DataFrame(forecast_sales_list, columns=["予測売上(円)"])

    # 順位と名前のDataFrameを結合
    result = pd.concat([rank_df, result], axis=1)

    x = range(0, 49)
    label=[1,2,3,4,5,6,7,8,9,10]
    height = data_forecast_sales.head(10).values
    fig, ax = plt.subplots()
    ax.bar(x,height, tick_label = label,width=0.7, color="g")
    ax.set_xlabel('rank')
    ax.set_ylabel('sales')
    ax.set_title('Basic Bar')
    ax.legend()
    plt.savefig('out.png')
    img = cv2.imread('out.png')

    # 予測結果をJSON形式で返す
    return result,img

    
def name():
    data = pd.read_csv('date_5.csv')
    sales = data.iloc[:, 3:]
    sales_names = sales.columns.tolist()
    return sales_names


@app.route("/pca", methods=["GET", "POST"])
def pca():
    if request.method == 'POST':
        dname = request.form.get('year')
        a,b = yosoku(int(dname))
        result = a
        result = pd.DataFrame(result, columns=["予測売上(円)"])
        sales_names = name() 
        for i in range(50):
            result.rename(index={i: sales_names[i]}, inplace=True)
        
        ranks = range(1, 50 + 1)
        ranks = pd.DataFrame(ranks)

        return render_template('pca.html', dname=dname, result=result,ranks=ranks)

@app.route("/test", methods=["GET", "POST"])
def gura():
        a,b = yosoku()
        img = b
        return render_template('test.html',img = img)

if __name__ == '__main__':
    app.debug = True
    app.run()



