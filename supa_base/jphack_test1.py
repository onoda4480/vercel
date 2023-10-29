#jphacks test
from supabase import Client, create_client
from datetime import datetime

SUPABASE_URL = "https://vusmwyplxywdcyksdbfu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ1c213eXBseHl3ZGN5a3NkYmZ1Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5Nzg5MjE3MSwiZXhwIjoyMDEzNDY4MTcxfQ.R-2CQ-vYkyzJ2WHmSbo2bU8ZBiPYt46msDHWeQuAfFQ"

today_time = datetime.now()
return_day = today_time.strftime("%Y-%m-%d")

# Supabaseクライアントを作成
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

list = []
#data = supabase.table("test_jphack").eq('name',"akiyosi").execute()
replay_Rental = supabase.table("Rental").select("id, lender_id, borrower_id, is_return, return_date, created_at").eq("return_date", return_day).execute()
data_Rental = replay_Rental.data

if data_Rental is not None:
    for row in data_Rental:
        list.append(row['lender_id'])
        print(row['lender_id'])

#replay_User = supabase.table("User").select("id, line_id, name, image_url").eq("return_date", return_day).execute()
#
#data_Rental = replay_Rental.data
print(data_Rental)
## name列の値を表示
#if data is not None:
#    for row in data:
#        list.append(row['name'])
#        print(row['name'])
##list.append(data)
##
#print(list)

