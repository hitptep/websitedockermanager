# 基于Python3.10镜像构建
FROM python:3.10

# 设置pip源
ARG PIP_INDEX_URL
ENV PIP_INDEX_URL ${PIP_INDEX_URL:-https://pypi.org/simple}

# 安装依赖
RUN pip install --upgrade pip

