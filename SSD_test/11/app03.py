import numpy as np
import pandas as pd
from flask import Flask, render_template, request
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import sample

sample.my_function()

app = Flask(__name__)

csv_file = 'C:/Users/sakuy/AppData/Local/Programs/Python/Python310/Scripts/year..csv'
df = pd.read_csv(csv_file, usecols=[0])
items = df['月'].to_list()

@app.route("/")
def show_toppage():
    return render_template('index.html', items=items)

@app.route("/pca", methods=["GET", "POST"])
def pca():
    if request.method == 'POST':
        dname = request.form.get('year')
        result = sample.my_function()
        return render_template('pca.html', dname=dname , result=result)
if __name__ == '__main__':
    app.run()

