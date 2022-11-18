

# WS server example

import asyncio
import json
import os
import websockets

async def get_json(websocket, path):
    data_json = await websocket.recv()
    data = json.loads(data_json)
    print("success!")
    os.system(f"bash ../implement/build.sh {data.image_name} {data.author_id} {data.container_name} {data.port} '{data.folder}' '{data.run_command}' '{data.cmd_command}'")
    greeting=1
    await websocket.send(greeting)

start_server = websockets.serve(get_json, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()