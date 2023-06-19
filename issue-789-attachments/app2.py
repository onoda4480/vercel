from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    choice = request.form.get('choice')
    if choice == '1月':
        result = '1月'
    elif choice == '2月':
        result = '2月。'
    elif choice == '3月':
        result = '3月。'
    elif choice == '4月':
        result = '4月。'
    elif choice == '5月':
        result = '5月。'
    elif choice == '6月':
        result = '6月。'
    elif choice == '7月':
        result = '7月。'
    elif choice == '8月':
        result = '8月。'    
    elif choice == '9月':
        result = '9月。'
    elif choice == '10月':
        result = '10月。'
    elif choice == '11月':
        result = '11月。'
    elif choice == '12月':
        result = '12月。'
    
    else:
        result = '無効な選択です。'
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run()

