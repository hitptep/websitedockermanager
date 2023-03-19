import asyncio
import json
import logging
import websockets

async def send_delete_image_request():
    uri = "ws://localhost:8799"
    async with websockets.connect(uri) as websocket:
        author = "myname"
        image = "myimage"
        request = {"author": author, "image": image}
        await websocket.send(json.dumps(request))
        response = await websocket.recv()
        print(f"Response: {response}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(send_delete_image_request())
