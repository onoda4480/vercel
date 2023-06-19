import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

bank_df = pd.read_csv('bank.csv', sep=',')
#print(bank_df.head)

bank_df=bank_df.dropna(subset=['job','education'])
bank_df = bank_df.dropna(thresh=2400, axis=1)
bank_df = bank_df.fillna({'contact':'unkown'})

bank_df = bank_df.replace('yes', 1)
bank_df = bank_df.replace('no', 0)
bank_df = bank_df[bank_df['age'] >= 18]
bank_df = bank_df[bank_df['age'] < 100]

#print(bank_df.head)

#ダミー変数
#bank_df_list=['job','marital','edcation','contact','month']
bank_df_job = pd.get_dummies(bank_df['job'])
bank_df_marital = pd.get_dummies(bank_df['marital'])
bank_df_education = pd.get_dummies(bank_df['education'])
bank_df_contact = pd.get_dummies(bank_df['contact'])
bank_df_month = pd.get_dummies(bank_df['month'])

#bank_df_list = [bank_df_job,bank_df_marital,bank_df_education,bank_df_contact,bank_df_month]


tmp1 = bank_df[['age', 'balance', 'housing', 'loan', 'day',
'duration', 'campaign', 'pdays', 'previous','y']]
print(tmp1.head())

tmp2 = pd.concat([tmp1,bank_df_marital],axis=1)
tmp3 = pd.concat([tmp2,bank_df_education],axis=1)
tmp4 = pd.concat([tmp3,bank_df_contact],axis=1)

bank_df_new = pd.concat([tmp4,bank_df_month],axis=1)

#bank_df_new = bank_df.replace('TRUE', 1)
#bank_df_new = bank_df.replace('FALSE', 0)
print(bank_df_new.head)
bank_df_new.to_csv('bank-prep.csv', index=False)



