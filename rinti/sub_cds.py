from concurrent.futures.process import BrokenProcessPool
import paho.mqtt.client as mqtt     # MQTTのライブラリをインポート

import signal
import numpy
import datetime
import sys

args = sys.argv

if len(args) > 1:
  BROKER = args[1]
else:
  BROKER = "localhost"

PORT = 1883
TOPIC = "top/cds1"
QOS = 0

cdsval = 0

# ブローカーに接続できたときの処理
def on_connect(client, userdata, flag, rc):
  print("Connected with result code " + str(rc))  # 接続できた旨表示
  client.subscribe(TOPIC, QOS)  # subするトピックを設定 

# ブローカーが切断したときの処理
def on_disconnect(client, userdata, rc):
  if  rc != 0:
    print("Unexpected disconnection.")

# メッセージが届いたときの処理
def on_message(client, userdata, msg):
	global cdsval
	# msg.topicにトピック名が，msg.payloadに届いたデータ本体が入っている
	cdsval = msg.payload.decode('utf-8')
	topic = msg.topic
	(top, cdsnum) = topic.split("/")
	dt_now = datetime.datetime.now()
	print(dt_now.strftime('%Y/%m/%d %H:%M:%S')," ",cdsnum,": ",cdsval)

# MQTTの接続設定
client = mqtt.Client()                 # クラスのインスタンス(実体)の作成
client.on_connect = on_connect         # 接続時のコールバック関数を登録
client.on_disconnect = on_disconnect   # 切断時のコールバックを登録
client.on_message = on_message         # メッセージ到着時のコールバック

client.connect(BROKER, PORT, 60)  # 接続先は自分自身

try:
    client.loop_forever()                  # 永久ループして待ち続ける
except KeyboardInterrupt:
    on_disconnect
    print("End.")
