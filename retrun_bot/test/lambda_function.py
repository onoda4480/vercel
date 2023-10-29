from line_tuuti import lineip
from supabot import base
from mainbot import main
import os

def lambda_handler():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    token = os.getenv("line_access_token")
    supabase, return_day, data= base(url,key)
    line_bot_api = lineip(token)
    main(data,supabase,return_day,line_bot_api)
