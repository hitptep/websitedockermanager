#!/bin/sh

#接收变量
image_name= #镜像选择
author_id=  #作者id
container_name= #容器名称
port= #开放端口,数组
folder= #项目文件夹路径
run_command=  #构建镜像执行命令
cmd_command=  #运行容器执行命令


#写入dockerfile
mkdir ~/workspace/dockerfile_folder/$author_id/$container_name
cd ~/workspace/dockerfile_folder/$author_id/$container_name
echo 'FROM base:$image_name' > dockerfile #重新构建
echo 'COPY * ~/workspace/' >> dockerfile
echo 'RUN $run_command' >> dockerfile
echo 'CMD cmd_command' >> dockerfile
for num in ${port[@]}
do
    echo 'EXPOSE $num' >> dockerfile
done


#构建
docker build -t $author_id:$container_name /workspace/docker_cp/$author_id/$container_name