import os
import json
import asyncio
import websockets
import docker

class DockerManager:
    def __init__(self):
        self.client = docker.from_env()

    def remove_container(self, name):
        try:
            container = self.client.containers.get(name)
            container.remove(force=True)
            return True, ''
        except docker.errors.NotFound:
            return False, 'container not found'
        except docker.errors.APIError as e:
            return False, str(e)


async def handler(websocket, path):
    docker_manager = DockerManager()

    async for message in websocket:
        try:
            data = json.loads(message)

            author = data.get('author')
            image = data.get('image')

            container_name = f"{author}:{image}"

            success, error = docker_manager.remove_container(container_name)

            response = {
                'author': author,
                'image': image,
                'code': 1 if success else -1 if error == 'container not found' else -2,
            }

            if not success:
                response['error'] = error

            await websocket.send(json.dumps(response))

        except Exception as e:
            print(str(e))


if __name__ == '__main__':
    start_server = websockets.serve(handler, 'localhost', 8798)

    print('ContainerDelete Server started')

    try:
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print('ContainerDelete Server stopped')
