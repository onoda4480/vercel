import pandas as pd
dat_df = pd.read_csv('energydata.csv',sep=',')
dat_df.head()
print(dat_df.shape)
print(dat_df.dtypes)

dat_df['date'] = pd.to_datetime(dat_df['date'],format = '%Y-%m-%d %H:%M:%S')
print(dat_df['date'])