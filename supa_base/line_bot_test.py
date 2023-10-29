from linebot import LineBotApi
from linebot.models import TextSendMessage
from datetime import datetime
# リモートリポジトリに"ご自身のチャネルのアクセストークン"をpushするのは、避けてください。
# 理由は、そのアクセストークンがあれば、あなたになりすまして、プッシュ通知を送れてしまうからです。
LINE_CHANNEL_ACCESS_TOKEN = "1hU6cN9xftNPzqyzti+CmO9t+WGazLwGd7uGWHXyl9D+kntAhpL5B8CsBekY98llONBNFTxQd+AoQNW0/8qGdPq3dJvfatJHblAYSzih8J+osdA5+qPOM7NqBqsmHUx6S1GDOQG09BVAxet6a5mEMQdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

today_time = datetime.now()
return_day = today_time.strftime("%Y-%m-%d")

def main():
    user_id = "U3d4c04d1ad2dfc143e72deb51d046b57"

    messages = TextSendMessage(text=f"今日が返却日です\n\n"
                                    f"返却日:{return_day}")
    line_bot_api.push_message(user_id, messages=messages)


if __name__ == "__main__":
    main()

