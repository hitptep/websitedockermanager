# PTEPDocker

## Communication

| 名称         | 类型   | Receive Data                                                 | Send Data              | 备注               |
| ------------ | ------ | ------------------------------------------------------------ | ---------------------- | ------------------ |
| ContainerRun | Server | json:作者id、镜像名、房间号                                  | null                   | 运行容器           |
| ImageBuild   | Server | json:基础镜像（如：latest）、作者id、私人镜像名、开放端口、文件夹、构建时命令、运行容器时命令 | 1                      | 镜像构建           |
| PortWatchdog | Server | Array:数据库中Port表                                         | Array:关闭的port的平台 | Docker监视程序     |
| sendPort     | Client |                                                              | Int：新开容器的Port    | 开启容器后返回Port |

