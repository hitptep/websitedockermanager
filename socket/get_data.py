#!/usr/bin/env python

# WS server example

import asyncio
import json

import websockets

async def get_json(websocket, path):
    data_json = await websocket.recv()
    data = json.loads(data_json)
    print("success!")
    greeting="Got"
    await websocket.send(greeting)

start_server = websockets.serve(get_json, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


