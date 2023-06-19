import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

bank_df = pd.read_csv('bank-prep.csv', sep=',')
bank_df.head() 
bank_df.tail(10) 

bank_df = bank_df.drop('y', axis=1) # y は目的変数のため対象外
sc = StandardScaler()
sc.fit(bank_df)
bank_df_sc = pd.DataFrame(sc.transform(bank_df), columns=bank_df.columns)
print(bank_df_sc.head())
print(bank_df_sc.describe())