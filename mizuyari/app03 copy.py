from flask import Flask, render_template, request
import os

app = Flask(__name__)
app.template_folder = os.path.abspath('template')


@app.route('/')
def index():
    return render_template('index.html')




@app.route('/second', methods=['POST'])
def sec():
    water_amount = request.form.get('water')
    time_amount = request.form.get('time')
    return render_template('result.html', water_amount=water_amount, time_amount=time_amount)

@app.route('/botan', methods=['POST'])
def water():
    water_amount = request.form.get('water')
    time_amount = request.form.get('time')
    print(water_amount)
    print(time_amount)
    return water_amount, time_amount



if __name__ == '__main__':
    app.run(debug=True)
