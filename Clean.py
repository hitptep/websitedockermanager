import docker
import time
import logging
import os
from datetime import datetime

# 设置日志文件名和位置
log_path = os.path.expanduser("~/.config/dockermanager/logs")
if not os.path.exists(log_path):
    os.makedirs(log_path)
log_file = f"{log_path}/Clean_{datetime.now().strftime('%Y-%m-%d')}.log"

# 配置logging
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# 获取docker客户端
client = docker.from_env()

def clean_unused_images():
    # 获取所有镜像列表
    images = client.images.list()

    # 过滤未使用且未被其他镜像依赖且未命名的镜像
    for image in images:
        tags = image.tags
        if tags:
            continue  # 跳过有tag的镜像
        if image.id in [x.id for x in client.containers.list(all=True)]:
            continue  # 跳过正在运行的容器所使用的镜像
        try:
            client.images.remove(image.id)
            logging.info(f"Removed unused image {image.id}")
        except Exception as e:
            logging.warning(f"Failed to remove unused image {image.id}: {str(e)}")

def main():
    while True:
        os.system("docker rm $(sudo docker ps -a -q)")
        clean_unused_images()
        time.sleep(10)

if __name__ == "__main__":
    main()
