import pandas as pd
df = pd.read_csv(
header=None,
sep='¥s+')
df.columns = ['CRIM', 'ZN', 'INDUS', 'CHAS', 
'NOX', 'RM', 'AGE', 'DIS', 'RAD', 
'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']
df.head()