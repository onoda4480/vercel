from ftplib import FTP_TLS
ENCODING = 'utf8'
open('rinti','wb')
config = {
    'host': '192.168.86.62',
    'user': 'yuuai2',
    'passwd': 'yuuaiseiki',
}

with FTP_TLS(**config) as ftp:
    with open('test', 'wb') as fp:
        ftp.retrbinary('RETR test', fp.write)



