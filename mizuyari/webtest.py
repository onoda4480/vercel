from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, Raspberry Pi!"

@app.route('/value/<data>')
def receive_value(data):
    # 受け取った値の処理
    return f"Received value: {data}"

if __name__ == '__main__':
    app.run(host='10.141.96.131')
