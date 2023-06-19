#!/usr/bin/env python
#coding: utf-8

import subprocess
import csv
import datetime
from time import sleep
import asyncio
import websockets

record_file_name = 'blt_detect.csv'
bltcount = 0

async def hello():
    uri = "ws://localhost:3030"
    async with websockets.connect(uri) as websocket:
        #時刻取得
                record_datetime = datetime.datetime.now()
                record_time = record_datetime.strftime('%Y%m%d-%X')

                cmd = 'hcitool con'
                res = subprocess.run(cmd.split())
                print(res)

            #検出するスマホのアドレス
                bd = 'F8:E9:4E:CD:E6:4C'

            #応答にスマホのアドレスが含まれているか？
                if(bd in res.decode()):
                    bltcount += 1
                    #GPIO.output(21,GPIO.HIGH)

                    #5回連続で受信したら記録
                    if(bltcount == 5):
                        print(record_time + bd)
                        #record_date
                        writer = csv.writer(open(record_file_name,'a'))
                        writer.writerow([record_time,bd,1])
                        var = input("1")
                        await websocket.send(var)
                        print (await websocket.recv())
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
            #GPIO.output(21,GPIO.LOW)

                    #record_date
                    writer = csv.writer(open(record_file_name,'a'))
                    writer.writerow([record_time,bd,0])
                    p1.kill()
                    p2.kill()
            
                sleep(6)
                cmd = "echo connect F8:E9:4E:CD:E6:4C| bluetoothctl"
                subprocess.call(cmd.split())

        #var = input("Please type your message: ")
        #await websocket.send(var)
        #print (await websocket.recv())
try:
    while True:
        asyncio.run(hello())
except KeyboardInterrupt:
    print("End.")
