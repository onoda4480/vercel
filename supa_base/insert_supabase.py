from supabase import Client, create_client

#supabase URL&key
SUPABASE_URL = "https://vusmwyplxywdcyksdbfu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ1c213eXBseHl3ZGN5a3NkYmZ1Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY5Nzg5MjE3MSwiZXhwIjoyMDEzNDY4MTcxfQ.R-2CQ-vYkyzJ2WHmSbo2bU8ZBiPYt46msDHWeQuAfFQ"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


supabase.table("User").insert(
   [
       {"id": "432413153151", "line_id": 'U3d4c04d1ad2dfc143e72deb51d046b57', "name": 'test_2', "image_url": ''},
       {"id": "131431413542", "line_id": 'U3d4c04d1ad2dfc143e72deb51d046b57', "name": 'test_3', "image_url": ''},
   ]
).execute()