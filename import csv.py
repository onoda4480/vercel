#import csv

# with open('bank.csv', 'r', encoding='utf-8') as f:
#     reader = csv.reader(f)
#     for row in reader:
#       print(row)
import pandas as pd
bank_df = pd.read_csv('bank.csv', sep=',')
bank_df.head() # CSVの先頭5行を表示
bank_df.tail(10) # CSVの末尾10行を表示
#print(bank_df.shape) # CSVの行数，列数
#print(bank_df.dtypes) # 各列の型
#print(bank_df.isnull().any(axis=1)) # 各行の欠損の有無
#print(bank_df.isnull().any(axis=0)) # 各列の欠損の有無
#print(bank_df.isnull().sum(axis=1)) # 各行の欠損の数
#print(bank_df.isnull().sum(axis=0)) # 各列の欠損の数
#print(bank_df.isnull().sum(axis=1).sort_values(ascending=True))
# 各行の欠損の数の多い順にソートしてみ

#print(bank_df.describe())
#print(bank_df.describe(include=[object]))

import matplotlib.pyplot as plt
#plt.hist(bank_df['age'])
#plt.xlabel('age')
#plt.ylabel('freq')
#plt.show()

#plt.scatter(bank_df['age'], bank_df['balance'])
#plt.xlabel('age')
#plt.ylabel('balance')
#plt.show()

#import matplotlib.pyplot as plt
#import pandas as pd
#import seaborn as sns

# データの読み込み
#data = pd.read_csv("bank.csv")

# 散布図行列を作成する
#sns.pairplot(data)

# グラフを表示する
#plt.show()


pd.plotting.scatter_matrix
y_yes = bank_df[bank_df['y']=='yes']
y_no = bank_df[bank_df['y']=='no']
y_age = [y_yes['age'], y_no['age']]
plt.boxplot(y_age, showmeans=True)
plt.xlabel('y')
plt.ylabel('age')
ax = plt.gca()
plt.setp(ax, xticklabels = ['yes', 'no'])
plt.show()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# データの作成
#np.random.seed(0)
#data = pd.read_csv("bank.csv")

# 散布図行列を作成する
#pd.plotting.scatter_matrix(data[['age', 'balance', 'day', 'duration']], alpha=0.8, figsize=(6, 6), diagonal='hist')

# グラフを表示する
#plt.show()

