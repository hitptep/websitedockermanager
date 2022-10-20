#!/bin/sh

room_id=88888
author_id=zhangzeyuan
container_name=test01

#润
docker run --name $author_id-$container_name-$room_id -P $author_id:$container_name

#虚拟局域网