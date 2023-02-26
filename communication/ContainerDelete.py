import os
import json
import logging
import asyncio
import websockets
import docker

# 日志设置
LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'
LOG_DIR = os.path.expanduser('~/.config/dockermanager/logs')

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, 'manager.log')),
        logging.StreamHandler()
    ]
)

containers_log = os.path.join(LOG_DIR, 'containers.log')


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
        logging.info(f"Received message: {message}")

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

            logging.info(f"Response: {response}")
            await websocket.send(json.dumps(response))

            with open(containers_log, 'a') as f:
                if success:
                    f.write(f"Container {container_name} removed\n")
                else:
                    f.write(f"Failed to remove container {container_name}: {error}\n")

        except Exception as e:
            logging.error(str(e))


if __name__ == '__main__':
    start_server = websockets.serve(handler, 'localhost', 8798)

    logging.info('ContainerDelete Server started')

    try:
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        logging.info('ContainerDelete Server stopped')
