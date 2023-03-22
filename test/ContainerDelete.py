import asyncio
import json
import websockets

async def send_message():
    async with websockets.connect('ws://localhost:8798') as websocket:
        id="74a83c5973865ad0682bb052117b0bfd726b217492bcaa26e8765bf606abedd5"
        message = id
        # 将消息转换为JSON字符串，并发送到WebSocket服务器
        await websocket.send(message)

        # 等待服务器返回响应
        response = await websocket.recv()
        json_response = json.loads(response)
        code = json_response['code']
        if code == 1:
            print(f"Container stopped successfully.")
        else:
            print(f"Container  not found.")

asyncio.get_event_loop().run_until_complete(send_message())
