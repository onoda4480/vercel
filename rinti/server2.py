#!/usr/bin/env python

import asyncio
import websockets
import subprocess

f_name = "./.temp.txt"

async def echo(websocket):
    async for message in websocket:
        print("<<< " + message)
        subprocess.run("/usr/games/fortune >" + f_name, shell=True)
        f = open(f_name,'r')
        message = f.readlines()
        for ret in message:
            print(">>> " + ret.strip())
            await websocket.send(ret.strip())
        f.close()

async def main():
    async with websockets.serve(echo, "localhost", 3030):
        await asyncio.Future()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("End.")