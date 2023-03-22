import json
import docker
import os
import asyncio
import websockets
from datetime import datetime

# WebSocket服务器地址
HOST = '0.0.0.0'
PORT = 8799

# Docker客户端
client = docker.from_env()

# 日志目录
LOG_DIR = os.path.expanduser('~/.config/dockermanager/logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


async def handle_delete_image(websocket, path):
    try:
        async for data in websocket:
            # 解析JSON数据
            data = json.loads(data)

            # 获取author和image
            author = data.get('author')
            image = data.get('image')

            # 删除镜像
            try:
                client.images.remove(f'{author}:{image}')
                code = 1
                error = None
            except docker.errors.ImageNotFound:
                code = -1
                error = 'image not found'
            except docker.errors.APIError as e:
                code = -1
                error = str(e)

            # 构造返回的JSON数据
            result = {
                'author': author,
                'image': image,
                'code': code
            }
            if error:
                result['error'] = error

            # 写入日志文件
            log_file = f'{LOG_DIR}/ImageDelete_{datetime.now().strftime("%Y-%m-%d")}.log'
            with open(log_file, 'a') as f:
                f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {author}/{image}\n')

            # 发送返回消息
            await websocket.send(json.dumps(result))
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # 启动WebSocket服务器
    start_server = websockets.serve(handle_delete_image, HOST, PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    print(f'WebSocket server started at {HOST}:{PORT}')

    # 运行事件循环
    asyncio.get_event_loop().run_forever()
