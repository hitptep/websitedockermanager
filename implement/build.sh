#!/bin/bash

##接收变量
#1= $1 #镜像选择
#2= $2  #作者id
#3= $3 #容器名称
#4= $4 #开放端口
#5= $5 #项目文件夹路径
#6= $6  #构建镜像执行命令
#7= $7  #运行容器执行命令


#写入dockerfile
mkdir ~/workspace/dockerfile_folder/$2
mkdir ~/workspace/dockerfile_folder/$2/$3
cd ~/workspace/dockerfile_folder/$2/$3
mkdir project
cp -f $5 ./project
echo 'FROM base:'$1'' > dockerfile #重新构建
echo 'COPY ./project /root/project' >> dockerfile
echo 'RUN '$6'' >> dockerfile
echo 'CMD cd /root/project && '$7'' >> dockerfile
echo 'EXPOSE '$4'' >> dockerfile


#构建
docker build -t $2:$3 .