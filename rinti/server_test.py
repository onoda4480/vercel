#!/usr/bin/env python

import asyncio
import websockets

f_name = "./.temp.txt"

async def echo(websocket):
    async for message in websocket:
        #print("<<< " + message)
        if message == '1':
            ret = "2kainiimasu。","."
            print(">>> " + ret)
            await websocket.send(ret)
async def main():
    async with websockets.serve(echo, "localhost", 3030):
        await asyncio.Future()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("End.")