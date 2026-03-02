
# Kubernetes 基础

## 概述

Kubernetes (K8s) 是一个开源的容器编排平台，用于自动化部署、扩展和管理容器化应用。

## 核心概念

### 1. Pod

Pod 是 K8s 的最小部署单元，包含一个或多个容器。

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
  - name: nginx
    image: nginx:1.19
    ports:
    - containerPort: 80
```

```bash
# 创建 Pod
kubectl apply -f pod.yaml

# 查看 Pod
kubectl get pods

# 查看 Pod 详情
kubectl describe pod my-pod

# 删除 Pod
kubectl delete pod my-pod
```

### 2. Deployment

Deployment 管理 Pod 的副本和更新。

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.19
        ports:
        - containerPort: 80
```

### 3. Service

Service 定义 Pod 的访问方式。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: nginx
  ports:
  - port: 80
    targetPort: 80
  type: LoadBalancer
```

## 常用命令

```bash
# 查看资源
kubectl get pods
kubectl get deployments
kubectl get services
kubectl get all

# 创建/更新资源
kubectl apply -f resource.yaml

# 删除资源
kubectl delete -f resource.yaml

# 查看日志
kubectl logs pod-name

# 进入容器
kubectl exec -it pod-name -- /bin/bash

# 扩缩容
kubectl scale deployment nginx --replicas=5
```

## 面试常见问题

1. **Pod 和容器的区别？**
   - Pod 是 K8s 的调度单元，可包含多个容器
   - 容器是运行时的隔离环境

2. **K8s 如何实现服务发现？**
   - 通过 Service 和 DNS
   - 每个 Service 有稳定的 DNS 名称

3. **什么是 Sidecar 模式？**
   - 在 Pod 中运行辅助容器
   - 用于日志收集、监控等功能

