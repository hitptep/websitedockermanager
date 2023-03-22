# API指南

### ImageBuild（构建镜像）

端口：8796

类型：服务端

接收：

```json
{
    "base":基础镜像,
    "author":作者,
    "image":作品名,
    "port":准备开放的端口（int）,
    "file":程序文件（压缩包或单个文件）位置,
    "run":构建镜像所用命令,
    "cmd":容器初始化命令
}
```

返回：

```json
{
    "author":作者,
    "image":作品名,
    "code":1代表成功。-1代表失败,
    "error":错误信息
}
```



### ContainerRun（运行容器）

端口：8797

类型：服务端

接收：

```json
{
    "author":作者,
    "image":作品名
}
```

返回：

```json
{
    "author":作者,
    "image":作品名,
    "code":1代表成功，-1代表失败,
    "id":容器ID,
    "port":容器映射到主机的端口（int），
    "error":错误信息
}
```

### 

### ContainerDelete（强制删除容器，正常情况下容器在作品程序退出后自动删除）

端口：8798

类型：服务端

接收（字符串类型）：

```字符串
"id":容器ID
```

返回：

```json
{
    "id":容器ID,
    "code":1代表成功，-1代表失败,
    "error":错误信息
}
```

### 

### ImageDelete（删除镜像）

类型：服务端

端口：8799

接收：

```json
{
    "author":作者,
    "image":作品名
}
```

返回：

```json
{
    "author":作者,
    "image":作品名,
    "code":1代表成功。-1代表失败,
    "error":错误信息
}
```



### Roomeye（监视容器运行情况）

类型：客户端

端口：8795

发送：

```json
{
    "author":作者,
    "image":作品名
    "id":容器ID
    "code":1正在运行，-1不在运行或不存在
    "close_reason":code为-1的原因
}
```

