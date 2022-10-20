#!/bin/sh

#接收变量
image_name="python" #镜像选择
author_id="zhangzeyuan"  #作者id
container_name="test01" #镜像名称
#port=["60001"] #开放端口,数组
folder="/home/zzy/upload/test/hello.py" #项目文件夹路径
run_command="echo no_run_command"  #构建镜像执行命令
cmd_command="python3 hello.py"  #运行容器执行命令


#写入dockerfile
mkdir /home/zzy/workspace/dockerfile_folder/$author_id
mkdir /home/zzy/workspace/dockerfile_folder/$author_id/$container_name
cd /home/zzy/workspace/dockerfile_folder/$author_id/$container_name
mkdir project
cp -f $folder ./project
echo 'FROM base:'$image_name'' > dockerfile #重新构建
echo 'COPY ./project /root/project' >> dockerfile
echo 'RUN '$run_command'' >> dockerfile
echo 'CMD cd /root/project && '$cmd_command'' >> dockerfile


#构建
docker build -t $author_id:$container_name .