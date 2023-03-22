import asyncio
import websockets
import json
import os
import random
import shutil
import subprocess
from datetime import datetime
import time

def nowtime():
    now=datetime.now()
    current_time = now.strftime("%Y-%m-%d~%H:%M:%S")
    return current_time

async def build_image(websocket, path):
    # receive the json from the websocket
    json_data = await websocket.recv()
    data = json.loads(json_data)

    # get the values from the json
    base = data['base']
    author = data['author']
    image = data['image']
    port = data['port']
    file = data['file']
    run = data['run']
    cmd = data['cmd']

    tmp_dir = os.path.expanduser(f"~/tmp/{author}/{image}")
    os.makedirs(tmp_dir, exist_ok=True)

    project_dir = os.path.join(tmp_dir, nowtime())
    os.makedirs(project_dir, exist_ok=True)

    # create the Dockerfile content
    dockerfile_content = f"FROM {base}\n"
    if port:
        dockerfile_content += "EXPOSE " + str(port) + "\n"
    if run:
        dockerfile_content += "RUN " + run + "\n"
    dockerfile_content += "CMD cd /root/project && " + cmd + "\n"
    dockerfile_content += "COPY ./"+nowtime()+" /root/project\n"

    # create the Dockerfile
    # tmp_dir = os.path.expanduser(f"~/tmp/{author}/{image}")
    # os.makedirs(tmp_dir, exist_ok=True)
    with open(os.path.join(tmp_dir, "Dockerfile"), "w") as f:
        f.write(dockerfile_content)

    # copy the file to the project directory
    # project_dir = os.path.join(tmp_dir,nowtime())
    # os.makedirs(project_dir, exist_ok=True)

    # if file is a compressed file, extract it
    if file.endswith(".zip"):
        subprocess.run(["unzip", "-K", "-q" ,file, "-d", project_dir], check=True)
        os.remove(file)
    else:
        shutil.copy(file, project_dir)

    # build the Docker image
    image_name = f"{author}:{image}"
    try:
        subprocess.run(["docker", "build", "-t", image_name, tmp_dir], check=True)
        code = 1
        error = ""
    except subprocess.CalledProcessError as e:
        code = -1
        error = str(e)

    shutil.rmtree(tmp_dir)
    # send the response back to the client
    response = {
        "author": author,
        "image": image,
        "code": code,
        "error": error
    }
    await websocket.send(json.dumps(response))

    # log the result
    log_dir = os.path.expanduser("~/.config/dockermanager/logs")
    os.makedirs(log_dir, exist_ok=True)
    # create the log file name with current date
    log_file = os.path.join(log_dir, 'ImageBuild_{}.log'.format(time.strftime('%Y-%m-%d')))

    with open(log_file, "a") as f:
        if code == 1:
            f.write(f"{nowtime()} - Built image {image_name}\n")
        else:
            f.write(f"{nowtime()} - Failed to build image {image_name}: {error}\n")


async def websocket_server():
    # start the websocket server
    async with websockets.serve(build_image, "localhost", 8796):
        # print("ImageBuild Server started.")
        await asyncio.Future()  # run forever

if __name__ == "__main__":

        asyncio.run(websocket_server())

