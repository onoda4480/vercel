#coding: utf-8
import subprocess
import csv
import datetime
from time import sleep
#import RPi.GPIO as GPIO

record_file_name = 'blt_detect.csv'
bltcount = 0

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(21,GPIO.OUT) #物理ピン40 BCM=21

try:
    while True:
        #時刻取得
        record_datetime = datetime.datetime.now()
        record_time = record_datetime.strftime('%Y%m%d-%X')

        cmd = 'hcitool con'
        res = subprocess.check_output(cmd.split())
        print(res)

        #検出するスマホのアドレス
        bd = '00:11:22:33:44:55'

        #応答にスマホのアドレスが含まれているか？
        if(bd in res.decode()):
            bltcount += 1
            #GPIO.output(21,GPIO.HIGH)

            #5回連続で受信したら記録
            if(bltcount == 5):
                print(record_time + ' ' + bd)
                #record_date
                writer = csv.writer(open(record_file_name,'a'))
                writer.writerow([record_time,bd,1])
                bltcount = 0
            else:
                pass
    
        else:
            p1 = subprocess.Popen(["echo","connect",bd], stdout=subprocess.PIPE,shell=True)
            p2 = subprocess.Popen(["bluetoothctl"], stdin=p1.stdout, stdout=subprocess.PIPE,shell=True)
            p1.stdout.close()
            outs,errs = p2.communicate()
            print('Attempt to connect...')
            bltcount = 0
            GPIO.output(21,GPIO.LOW)

            #record_date
            writer = csv.writer(open(record_file_name,'a'))
            writer.writerow([record_time,bd,0])
            p1.kill()
            p2.kill()
            
        sleep(6)
    
except KeyboardInterrupt:
    pass