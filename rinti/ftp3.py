from ftplib import FTP
import itertools
from time import sleep
import datetime
FTP.encoding = "utf-8"
ENCODING = 'utf8'
dt = datetime.date.today()

while True:
    ftp = FTP('192.168.86.62')
    ftp.set_pasv('true')
    ftp.login('yuuai', 'yuuaiseiki')
    #file_list = ftp.nlst(".")
    #print(file_list)
    #encoding = "utf-8"
    with open("logfile"+ str(dt) +".csv", "wb") as f:
        ftp.retrbinary("RETR /home/yuuai/ダウンロード/IPUT_Work-naoki/logfile.csv", f.write)
    #encoding = "utf-8"
    ftp.close()
    sleep(5)