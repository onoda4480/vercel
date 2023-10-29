import pandas as pd
bank_df = pd.read_csv('tarvel+review+ratings\google_review_ratings.csv', sep=',')
bank_df.head() # CSVの先頭5行を表示
bank_df.tail(10) # CSVの末尾10行を表示
print(bank_df.shape) # CSVの行数，列数
print(bank_df.dtypes) # 各列の型
print(bank_df.isnull().any(axis=1)) # 各行の欠損の有無
print(bank_df.isnull().any(axis=0)) # 各列の欠損の有無
print(bank_df.isnull().sum(axis=1)) # 各行の欠損の数
print(bank_df.isnull().sum(axis=0)) # 各列の欠損の数
print(bank_df.isnull().sum(axis=1).sort_values(ascending=False))# 各行の欠損の数の多い順にソートしてみましょう

import matplotlib.pyplot as plt
plt.hist(bank_df['parks'])
plt.xlabel('parks')
plt.ylabel('freq')
plt.show()
