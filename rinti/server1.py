#!/usr/bin/env python

import asyncio
import websockets

f_name = "./.temp.txt"

async def echo(websocket):
    async for message in websocket:
        print("<<< " + message)
        ret = message
        #print(">>> " + ret)
        if ret == "1":
            print("Hello")
            await websocket.send(ret)
        else:
            await websocket.send(ret)

async def main():
    async with websockets.serve(echo, "localhost", 3030):
        await asyncio.Future()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("End.")