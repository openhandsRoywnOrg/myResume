
# Docker Compose

## 概述

Docker Compose 是用于定义和运行多容器 Docker 应用的工具。

## 基本使用

### 1. docker-compose.yml 示例

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/code
    environment:
      - FLASK_ENV=development
    depends_on:
      - redis

  redis:
    image: "redis:alpine"
    ports:
      - "6379:6379"
```

### 2. 常用命令

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 查看日志
docker-compose logs -f

# 重启服务
docker-compose restart

# 构建镜像
docker-compose build

# 查看运行状态
docker-compose ps
```

## 网络配置

```yaml
version: '3.8'

services:
  frontend:
    image: nginx
    networks:
      - frontend-net

  backend:
    image: node
    networks:
      - frontend-net
      - backend-net

  database:
    image: postgres
    networks:
      - backend-net

networks:
  frontend-net:
  backend-net:
```

## 面试常见问题

1. **Docker Compose 和 Docker Swarm 的区别？**
   - Compose 用于本地多容器应用
   - Swarm 是 Docker 的原生集群管理工具

2. **如何管理环境变量？**
   - 使用 .env 文件
   - 在 docker-compose.yml 中定义
   - 使用 env_file 指令

3. **如何实现服务依赖？**
   - 使用 depends_on 指令
   - 使用健康检查确保服务就绪

