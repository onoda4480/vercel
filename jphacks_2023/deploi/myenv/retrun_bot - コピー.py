from linebot import LineBotApi
from linebot.models import TextSendMessage
from datetime import datetime
from supabase import Client, create_client
from datetime import datetime

# リモートリポジトリに"ご自身のチャネルのアクセストークン"をpushするのは、避けてください。
# 理由は、そのアクセストークンがあれば、あなたになりすまして、プッシュ通知を送れてしまうからです。
#line bot token
LINE_CHANNEL_ACCESS_TOKEN = "1hU6cN9xftNPzqyzti+CmO9t+WGazLwGd7uGWHXyl9D+kntAhpL5B8CsBekY98llONBNFTxQd+AoQNW0/8qGdPq3dJvfatJHblAYSzih8J+osdA5+qPOM7NqBqsmHUx6S1GDOQG09BVAxet6a5mEMQdB04t89/1O/w1cDnyilFU="

#supabase URL&key
SUPABASE_URL = "https://vusmwyplxywdcyksdbfu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ1c213eXBseHl3ZGN5a3NkYmZ1Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5Nzg5MjE3MSwiZXhwIjoyMDEzNDY4MTcxfQ.R-2CQ-vYkyzJ2WHmSbo2bU8ZBiPYt46msDHWeQuAfFQ"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
# Supabaseクライアントを作成
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

today_time = datetime.now()
return_day = today_time.strftime("%Y-%m-%d")

#data = supabase.table("test_jphack").eq('name',"akiyosi").execute()
replay_Rental = supabase.table("Rental").select("id, borrower_id").eq("return_date", return_day).execute()
data = replay_Rental.data
#print(data)

list_id = []
list_line_id = []

# name列の値を表示
def main(data):
    if data is not None:
        for row in data:
            rental_id = f"{row['id']}"
            replay_User = supabase.table("User").select("id, line_id, name, image_url").eq("id", row['borrower_id']).execute()
            data_User = replay_User.data
            for row in data_User:
                list_line_id.append(row['line_id'])
                #print(row['line_id'])
                user_id = f"{row['line_id']}"
                user_name = f"{row['name']}"
                #print(user_id)
                #print(list_line_id)
                liff_url = f"https://liff/{rental_id}"
                messages = TextSendMessage(text=f"{user_name}""さんから借りた本は今日が返却日です\n\n"
                                            f"返却日:{return_day}\n\n"
                                            f"{liff_url}")
                line_bot_api.push_message(user_id, messages=messages)


if __name__ == "__main__":
    main(data)
