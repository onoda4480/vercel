from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# サンプルのDataFrame
data = {'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35]}
df = pd.DataFrame(data)
print(df)

@app.route('/')
def show_dataframe():
    table_html = df.to_html()
    return render_template('flask/templates/index.html', table_html=table_html)

if __name__ == '__main__':
    app.run()
