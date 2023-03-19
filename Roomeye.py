import os
import json
import logging
import threading
import time
import docker
import websocket

def get_container_info(container):
    """获取容器信息"""
    info = {
        'id': container.id,
        'name': container.name,
        'image': container.image.tags[0],
    }
    return info

def on_message(ws, message):
    """WebSocket客户端收到消息"""
    pass

def on_error(ws, error):
    """WebSocket客户端发生错误"""
    logging.error(error)

def on_close(ws):
    """WebSocket客户端关闭"""
    logging.info('WebSocket closed')

def on_open(ws):
    """WebSocket客户端打开"""
    logging.info('WebSocket opened')

def monitor():
    """监视Docker容器的运行状态"""
    log_dir = os.path.expanduser('~/.config/dockermanager/logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_filename = os.path.join(log_dir, 'Containers_{}.log'.format(time.strftime('%Y-%m-%d')))

    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s %(message)s')
    client = docker.from_env()
    while True:
        containers = client.containers.list(all=True)
        for container in containers:
            container_info = get_container_info(container)
            if container.status == 'running':
                code = 1
                close_reason = None
            else:
                code = 0
                close_reason = container.status
            data = {
                'name': container_info['image'],
                'id': container_info['id'],
                'code': code,
                'close_reason': close_reason,
            }
            logging.info(json.dumps(data))
            ws.send(json.dumps(data))
        time.sleep(1)

if __name__ == '__main__':
    t = threading.Thread(target=monitor)
    t.daemon = True
    t.start()

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8795",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
