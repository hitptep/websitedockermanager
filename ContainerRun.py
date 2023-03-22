import os
import json
import random
import socket

import docker
import time
import threading
import asyncio
import websockets
from docker import client

import logging
from datetime import datetime

class ContainerRunServer:
    def __init__(self, port):
        self.port = port
        self.docker_client = docker.from_env()
        self.log_dir = os.path.expanduser("~/.config/dockermanager/logs")
        self.log_file = os.path.join(self.log_dir, f"ContainerRun_{datetime.now().strftime('%Y-%m-%d')}.log")
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        logging.basicConfig(filename=self.log_file, level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    def start(self):
        logging.info("ContainerRun Server started.")
        asyncio.get_event_loop().run_until_complete(self.run_server())

    def stop(self):
        logging.info("ContainerRun Server stopped.")

    async def run_server(self):
        async with websockets.serve(self.handle_request, "0.0.0.0", self.port):
            await asyncio.Future()  # run forever

    def get_free_port(self):
        """
        获取当前未使用的端口
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]

    async def handle_request(self, websocket, path):
        try:
            request = await websocket.recv()
            data = json.loads(request)
            author = data.get('author')
            image_name = data.get('image')
            logging.info(f"Received request for image {author}:{image_name}")

            port = None
            image = self.docker_client.images.get(f"{author}:{image_name}")
            exposed_ports = list(image.attrs['Config']['ExposedPorts'].keys())

            # 获取一个未使用的端口
            if exposed_ports[0]:
                port=self.get_free_port()

                container = self.docker_client.containers.run(
                    f"{author}:{image_name}",
                    detach=True,
                    auto_remove=True,
                    ports={exposed_ports[0]: port},
                )
            else:
                container = self.docker_client.containers.run(
                    f"{author}:{image_name}",
                    detach=True,
                    auto_remove=True,
                )
            container_id = container.id
            # container.stop_callback = lambda reason: logging.warning(f"Container stopped: {reason}")
            logging.info(f"Container started: {author}:{image_name} (ID: {container_id})")
            response = {"author": author, "image": image_name, "code": 1, "id": container_id}  # 将容器ID添加到JSON对象中
            if port:
                response["port"] = port

            # log_path = os.path.expanduser(
            #     "~/.config/dockermanager/logs/Containers_" + time.strftime("%Y-%m-%d") + ".log")
            # with open(log_path, "a") as log_file:
            #     log_file.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] WARNING: Container {container_id} stopped\n")

            await websocket.send(json.dumps(response))

        except Exception as e:
            logging.error(f"Error handling request: {e}")
            error = {"code": -1, "error": str(e)}
            await websocket.send(json.dumps(error))


if __name__ == "__main__":
    server = ContainerRunServer(8797)
    server.start()
