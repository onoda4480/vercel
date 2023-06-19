import pandas as pd
import matplotlib.pyplot as plt

bank_df = pd.read_csv('bank.csv', sep=',')
bank_df.head() 
bank_df.tail(10) 

# データの作成
#np.random.seed(0)

# 散布図行列を作成する
pd.plotting.scatter_matrix(bank_df[['age', 'balance', 'day', 'duration']], alpha=0.8, figsize=(6, 6), diagonal='hist')

# グラフを表示する
plt.show()
