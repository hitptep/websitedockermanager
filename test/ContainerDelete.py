import asyncio
import json
import websockets

async def send_message():
    async with websockets.connect('ws://localhost:8798') as websocket:
        author = 'author1'
        image = 'image1'
        message = {
            'author': author,
            'image': image
        }
        # 将消息转换为JSON字符串，并发送到WebSocket服务器
        await websocket.send(json.dumps(message))

        # 等待服务器返回响应
        response = await websocket.recv()
        json_response = json.loads(response)
        code = json_response['code']
        if code == 1:
            print(f"Container {author}:{image} stopped successfully.")
        else:
            print(f"Container {author}:{image} not found.")

asyncio.get_event_loop().run_until_complete(send_message())
