import pandas as pd
import matplotlib.pyplot as plt

bank_df = pd.read_csv('bank.csv', sep=',')
#bank_df.head() 
#bank_df.tail(10) 
bank_df=bank_df.dropna(subset=['job','education'])
bank_df = bank_df.dropna(thresh=2400, axis=1)
print(bank_df.shape)


#欠損値の閾値は thresh で指定
#xis=1 で（行ではなく）列を対象とできる
#hresh=2400, axis=1
#bank_df = bank_df.dropna(thresh=2400, axis=1)