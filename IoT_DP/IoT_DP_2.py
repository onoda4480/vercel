import pandas as pd
import matplotlib.pyplot as plt

bank_df = pd.read_csv('bank.csv', sep=',')

bank_df = bank_df[bank_df['age'] >= 18]
bank_df = bank_df[bank_df['age'] < 100]

pd.plotting.scatter_matrix
y_yes = bank_df[bank_df['y']=='yes']
y_no = bank_df[bank_df['y']=='no']
y_age = [y_yes['age'], y_no['age']]
y_balance = [y_yes['balance'], y_no['balance']]
y_day = [y_yes['day'], y_no['day']]
y_duration = [y_yes['duration'], y_no['duration']]
y_campaign = [y_yes['campaign'], y_no['campaign']]
y_pdays = [y_yes['pdays'], y_no['pdays']]
y_previous = [y_yes['previous'], y_no['previous']]

list_y =[y_age,y_balance,y_day,y_duration,y_campaign,y_pdays,y_previous]
list_a = ['age',"balance","day","duration","campaign","pdays","previous"]

bank_df.describe

i = 0
for i in  range(len(list_y)):
    plt.boxplot(list_y[i],showmeans=True)
    plt.xlabel('y')
    plt.ylabel(list_a[i])
    ax = plt.gca()
    plt.setp(ax, xticklabels = ['yes', 'no'])
    plt.show()


