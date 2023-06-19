#!/usr/bin/env python

import asyncio
import websockets
import subprocess

f_name = "./.temp.txt"

async def echo(websocket):
    async for message in websocket:
        print("<<< " + message)
        ft = subprocess.run("/usr/games/fortune", capture_output=True, encoding="utf-8")
        ret = str(ft.stdout).strip()
        print(">>> " + ret)
        await websocket.send(ret)

async def main():
    async with websockets.serve(echo, "localhost", 3030):
        await asyncio.Future()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("End.")