import os
import json
import docker
import time
import threading
import asyncio
import websockets


class ContainerRunServer:
    def __init__(self, port):
        self.port = port
        self.docker_client = docker.from_env()

    def start(self):
        print("ContainerRun Server started.")
        asyncio.get_event_loop().run_until_complete(self.run_server())

    def stop(self):
        print("ContainerRun Server stopped.")

    async def run_server(self):
        async with websockets.serve(self.handle_request, "0.0.0.0", self.port):
            await asyncio.Future()  # run forever

    async def handle_request(self, websocket, path):
        try:
            request = await websocket.recv()
            data = json.loads(request)
            author = data.get('author')
            image = data.get('image')
            print(f"Received request for image {author}/{image}")

            container = self.docker_client.containers.run(
                f"{author}/{image}",
                detach=True,
                auto_remove=True,
                ports={},
            )

            container_id = container.id  # 获取容器ID

            port = None
            if container.attrs["NetworkSettings"]["Ports"]:
                port = container.attrs["NetworkSettings"]["Ports"]["80/tcp"][0]["HostPort"]
                print(f"Container running on port {port}")
            else:
                print("No ports are exposed in the container")

            # Set the stop callback function to log the reason for stopping the container
            container.stop_callback = lambda reason: print(f"Container stopped: {reason}")

            response = {"author": author, "image": image, "code": 1, "id": container_id}  # 将容器ID添加到JSON对象中
            if port:
                response["port"] = port

            await websocket.send(json.dumps(response))

        except Exception as e:
            print(f"Error handling request: {e}")
            error = {"code": -1, "error": str(e)}
            await websocket.send(json.dumps(error))


        except Exception as e:
            print(f"Error handling request: {e}")
            error = {"code": -1, "error": str(e)}
            await websocket.send(json.dumps(error))


if __name__ == "__main__":
    server = ContainerRunServer(8797)
    server.start()
