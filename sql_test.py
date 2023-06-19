import pprint
import pyodbc
import pandas as pd

def login():
    driver='{SQL Server}'
    server = 'WNK210094\SQLEXPRESS'
    database = 'test'
    trusted_connection='yes'

    connect= pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';PORT=1433;Trusted_Connection='+trusted_connection+';')
    cursor = connect.cursor()
    cursor.execute( "SELECT * FROM date_1" )
    rows = cursor.fetchall()
    pprint.pprint( rows )
    #df = pd.DataFrame(rows)
    cursor.close()
    connect.close()
    return rows

if __name__ == '__main__':
    rows = login()
    df_a = pd.DataFrame(rows)
    print(df_a)

