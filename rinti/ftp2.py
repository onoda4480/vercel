import ftplib
import itertools
from time import sleep

ftp = ftplib.FTP('192.168.86.62')
ftp.set_pasv('true')
ftp.login('yuuai2', 'yuuaiseiki')

#file_list = ftp.nlst(".")
#print(file_list)

with open("test2.txt", "w") as f:
    ftp.retrlines("RETR /home/yuuai2/test2.txt", f.write)
ftp.close()
