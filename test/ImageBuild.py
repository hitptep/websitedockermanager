import asyncio
import websockets


async def send_receive():
    uri = "ws://localhost:8796"
    async with websockets.connect(uri) as websocket:
        # Send a message to the server
        message = '{"base": "base:python3.10", "author": "zzy", "image": "i2", "port": 8080, "file": "/home/ubuntu/dockermanager/test/index.zip", "run": "echo \'hello world\'", "cmd": "python3 -m http.server 8080"}'
        print(f"Sending message: {message}")
        await websocket.send(message)

        # Receive a message from the server
        response = await websocket.recv()
        print(f"Received message: {response}")

        # Close the connection
        await websocket.close()


asyncio.get_event_loop().run_until_complete(send_receive())
