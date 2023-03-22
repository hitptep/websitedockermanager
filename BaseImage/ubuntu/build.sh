#!/bin/bash

# 定义Docker镜像名称和版本号
IMAGE_NAME="base"
IMAGE_VERSION="ubuntu"

# 构建Docker镜像
docker build \
  -t "${IMAGE_NAME}:${IMAGE_VERSION}" \
  .

# 打印Docker镜像列表
docker images
