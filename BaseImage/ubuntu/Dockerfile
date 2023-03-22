FROM ubuntu:latest

# 设置apt源
RUN sed -i 's/archive.ubuntu.com/mirrors.tencentyun.com/g' /etc/apt/sources.list

# 安装常用软件包
RUN apt-get update && \
    apt-get install -y \
    wget \
    curl \
    git

# 清理缓存
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*
