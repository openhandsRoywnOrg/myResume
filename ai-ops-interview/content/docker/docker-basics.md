
# Docker 基础

## 概述

Docker 是一个开源的容器化平台，用于构建、部署和运行应用程序。

## 核心概念

### 1. 镜像 (Image)

镜像是只读模板，包含运行应用所需的代码、运行时、库和配置。

```bash
# 拉取镜像
docker pull nginx:latest

# 查看镜像
docker images

# 删除镜像
docker rmi image_id
```

### 2. 容器 (Container)

容器是镜像的运行实例。

```bash
# 运行容器
docker run -d -p 80:80 --name my-nginx nginx

# 查看容器
docker ps
docker ps -a

# 停止/启动容器
docker stop container_id
docker start container_id

# 删除容器
docker rm container_id
```

### 3. Dockerfile

Dockerfile 是构建镜像的脚本。

```dockerfile
FROM ubuntu:20.04
LABEL maintainer="example@example.com"

RUN apt-get update && apt-get install -y python3

WORKDIR /app
COPY . /app

CMD ["python3", "app.py"]
```

```bash
# 构建镜像
docker build -t my-app .
```

## 数据卷 (Volume)

```bash
# 创建数据卷
docker volume create my-volume

# 挂载数据卷
docker run -v my-volume:/data my-app

# 查看数据卷
docker volume ls
```

## 网络

```bash
# 创建网络
docker network create my-network

# 连接容器到网络
docker network connect my-network container_id
```

## 面试常见问题

1. **Docker 和虚拟机的区别？**
   - Docker 容器共享主机内核，更轻量
   - 虚拟机有完整的操作系统，更重

2. **Docker 的分层存储是什么？**
   - 镜像由多个只读层组成
   - 容器在最上层添加可写层

3. **如何优化 Docker 镜像大小？**
   - 使用多阶段构建
   - 选择基础镜像（如 alpine）
   - 清理不必要的文件

