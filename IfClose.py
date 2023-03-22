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

class ContainerCloseLogger:
    def __init__(self, log_dir):
        self.log_dir = log_dir
        self.docker_client = docker.from_env()
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            filename=os.path.join(self.log_dir, f"ContainerClose_{time.strftime('%Y-%m-%d')}.log"),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def start(self):
        print("ContainerCloseLogger started.")
        for container in self.docker_client.containers.list():
            self.attach_stop_listener(container)
        for event in self.docker_client.events():
            self.handle_event(json.loads(event.decode('utf-8')))

    def stop(self):
        print("ContainerCloseLogger stopped.")

    def attach_stop_listener(self, container):
        container.stop_callback = lambda reason: self.log_container_close(container, reason)

    def handle_event(self, event):
        if event["Type"] == "container" and event["Action"] in ["stop", "die"]:
            container = self.docker_client.containers.get(event["id"])
            self.log_container_close(container, event["Action"])

    def log_container_close(self, container, reason):
        if reason == "die":
            level = logging.WARNING
        else:
            level = logging.INFO
        image_name = container.image.attrs["RepoTags"][0]
        container_id = container.id
        close_time = time.strftime('%Y-%m-%d %H:%M:%S')
        message = f"Container {container_id} (image: {image_name}) closed due to {reason} at {close_time}."
        logging.log(level, message)


if __name__ == "__main__":
    logger = ContainerCloseLogger(os.path.expanduser("~/.config/dockermanager/logs"))
    logger.start()
