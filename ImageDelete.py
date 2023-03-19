import threading
import websocket
import json
import docker
import os
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

class WebSocketServer(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port

    def run(self):
        websocket.enableTrace(True)
        server = websocket.WebSocketServer(self.host, self.port, WebSocketHandler)
        server.serve_forever()

class WebSocketHandler:
    def __init__(self, client, server):
        self.client = client
        self.server = server

    def handleMessage(self):
        # 处理消息
        try:
            # 解析JSON数据
            data = json.loads(self.data)

            # 获取author和image
            author = data.get('author')
            image = data.get('image')

            # 删除镜像
            try:
                client.images.remove(f'{author}/{image}')
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

            return json.dumps(result)
        except Exception as e:
            return json.dumps({'code': -1, 'error': str(e)})

    def handleConnected(self):
        print(f'Client {self.client_address[0]} connected')

    def handleClose(self):
        print(f'Client {self.client_address[0]} closed')

if __name__ == '__main__':
    # 启动WebSocket服务器
    server = WebSocketServer(HOST, PORT)
    server.start()
    print(f'WebSocket server started at {HOST}:{PORT}')
