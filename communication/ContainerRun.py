import os
import json
import docker
import time
import logging
import threading
import asyncio
import websockets


class ContainerRunServer:
    def __init__(self, port):
        self.port = port
        self.docker_client = docker.from_env()
        self.logger = logging.getLogger("ContainerRun")

    def start(self):
        self.logger.info("ContainerRun Server started.")
        asyncio.get_event_loop().run_until_complete(self.run_server())

    def stop(self):
        self.logger.info("ContainerRun Server stopped.")

    async def run_server(self):
        async with websockets.serve(self.handle_request, "0.0.0.0", self.port):
            await asyncio.Future()  # run forever

    async def handle_request(self, websocket, path):
        try:
            request = await websocket.recv()
            data = json.loads(request)
            author = data.get('author')
            image = data.get('image')
            self.logger.info(f"Received request for image {author}/{image}")

            container = self.docker_client.containers.run(
                f"{author}/{image}",
                detach=True,
                auto_remove=True,
                ports={},
            )

            port = None
            if container.attrs["NetworkSettings"]["Ports"]:
                port = container.attrs["NetworkSettings"]["Ports"]["80/tcp"][0]["HostPort"]
                self.logger.info(f"Container running on port {port}")
            else:
                self.logger.info("No ports are exposed in the container")

            # Set the stop callback function to log the reason for stopping the container
            container.stop_callback = lambda reason: self.logger.info(f"Container stopped: {reason}")

            response = {"author": author, "image": image, "code": 1}
            if port:
                response["port"] = port

            await websocket.send(json.dumps(response))

        except Exception as e:
            self.logger.exception(f"Error handling request: {e}")
            error = {"code": -1, "error": str(e)}
            await websocket.send(json.dumps(error))


if __name__ == "__main__":
    logging.basicConfig(filename=os.path.expanduser("~/.config/dockermanager/logs/manager.log"),
                        level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    server = ContainerRunServer(8797)
    server.start()
