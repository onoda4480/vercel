#!/usr/bin/env python

import asyncio
import websockets

async def hello():
    uri = "ws://localhost:3030"
    async with websockets.connect(uri) as websocket:
        var = input("Please type your message: ")
        await websocket.send(var)
        print (await websocket.recv())
try:
    while True:
        asyncio.run(hello())
except KeyboardInterrupt:
    print("End.")
