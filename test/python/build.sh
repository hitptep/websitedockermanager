#!/bin/bash

# 定义Docker镜像名称和版本号
IMAGE_NAME="base"
IMAGE_VERSION="python3.10"

# 构建Docker镜像
docker build \
  --build-arg PYTHON_VERSION=3.10 \
  --build-arg PIP_INDEX_URL=https://mirrors.cloud.tencent.com/pypi/simple \
  -t "${IMAGE_NAME}:${IMAGE_VERSION}" \
  .

# 打印Docker镜像列表
docker images
