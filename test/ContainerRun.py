import asyncio
import websockets
import json

async def send_receive():
    async with websockets.connect('ws://localhost:8797') as websocket:
        # 构造要发送的JSON数据
        data = {"author": "myname", "image": "myimage"}
        # 将字典转换为JSON字符串，并发送
        await websocket.send(json.dumps(data))
        print(f"Sending message: {json.dumps(data)}")

        # 等待接收服务器响应
        response = await websocket.recv()
        print(f"Received message: {response}")

asyncio.get_event_loop().run_until_complete(send_receive())
