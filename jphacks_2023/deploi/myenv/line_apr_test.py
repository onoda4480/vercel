import os
from linebot import LineBotApi

def lineip():
    token = os.getenv("LenBow_token")
    if token:
        line_bot_api = LineBotApi(token)
        return line_bot_api
    else:
        print("LenBow_token 環境変数が設定されていません。")
        return None

# LINE Bot API を取得
line_bot_api = lineip()

if line_bot_api:
    print("LINE Bot API が正常に設定されました。")
else:
    print("LINE Bot API の設定に問題があります。")
