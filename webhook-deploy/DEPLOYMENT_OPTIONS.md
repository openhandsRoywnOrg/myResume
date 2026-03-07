# Webhook Server 部署方案对比

## 问题背景

Webhook Server 运行在 Docker 容器内，但 `openhands` 命令安装在宿主机上，导致容器内无法调用宿主机的命令。

## 解决方案

### 方案 1: 宿主机模式（推荐）⭐

**描述**: 直接在宿主机运行 webhook server，不使用 Docker

**适用场景**:
- ✅ `openhands` 已安装在宿主机
- ✅ 希望简化部署
- ✅ 不需要容器隔离

**部署方法**:
```bash
cd webhook-deploy
export WEBHOOK_SECRET="your-secret"
./deploy-host.sh
```

**优势**:
- ✅ 简单直接，无需 Docker
- ✅ 可以直接调用宿主机的 `openhands` 命令
- ✅ 性能更好，无容器开销
- ✅ 日志文件在 `/tmp/webhook_server.log`

**劣势**:
- ⚠️ 需要 Python 环境
- ⚠️ 依赖宿主机系统

**文件**:
- `deploy-host.sh` - 宿主机部署脚本

---

### 方案 2: Docker 容器模式

**描述**: 在容器内安装 `openhands-ai`，完全容器化

**适用场景**:
- ✅ 需要容器隔离
- ✅ 希望环境一致
- ✅ 宿主机是 Windows/Mac

**部署方法**:
```bash
cd webhook-deploy
export WEBHOOK_SECRET="your-secret"
./deploy-webhook-v2.sh
```

**优势**:
- ✅ 环境隔离
- ✅ 跨平台一致
- ✅ 易于管理

**劣势**:
- ⚠️ 需要在容器内安装 `openhands-ai`
- ⚠️ 容器启动时需要安装依赖（较慢）
- ⚠️ 无法直接使用宿主机的配置

**文件**:
- `deploy-webhook-v2.sh` - Docker 部署脚本

**修改建议**:
当前脚本已经配置为在容器内安装 `openhands-ai`：
```bash
bash -c "pip install flask openhands-ai && python /app/webhook_server.py"
```

---

### 方案 3: 混合模式（不推荐）

**描述**: 容器通过 SSH 或 HTTP 调用宿主机的 `openhands`

**实现方式**:
1. SSH 方式：配置容器到宿主机的 SSH 免密
2. HTTP 方式：在宿主机运行 HTTP 服务

**不推荐原因**:
- ❌ 配置复杂
- ❌ 增加故障点
- ❌ 性能开销

---

## 推荐方案

### 如果宿主机是 Linux 且已安装 openhands

**选择**: 方案 1 - 宿主机模式

**理由**:
- 最简单
- 性能最好
- 可以直接使用现有配置

**部署命令**:
```bash
# SSH 登录到服务器 42.194.162.251
ssh root@42.194.162.251

# 停止 Docker 容器（如果正在运行）
docker stop openhands-webhook-server

# 部署宿主机版本
cd /path/to/webhook-deploy
export WEBHOOK_SECRET="a25b34e37c82e8b17e98a04615380db6ffeb5c2ccba0b428172c1c637b8d4796"
./deploy-host.sh
```

---

### 如果需要容器化

**选择**: 方案 2 - Docker 容器模式

**理由**:
- 环境隔离
- 易于管理
- 跨平台

**部署命令**:
```bash
# SSH 登录到服务器 42.194.162.251
ssh root@42.194.162.251

# 部署 Docker 版本
cd /path/to/webhook-deploy
export WEBHOOK_SECRET="a25b34e37c82e8b17e98a04615380db6ffeb5c2ccba0b428172c1c637b8d4796"
./deploy-webhook-v2.sh
```

**注意**: 容器会在启动时自动安装 `openhands-ai`，首次启动可能需要几分钟。

---

## 快速对比

| 特性 | 宿主机模式 | Docker 模式 |
|------|----------|-----------|
| **部署复杂度** | ⭐ 简单 | ⭐⭐ 中等 |
| **性能** | ⭐⭐⭐ 最佳 | ⭐⭐ 有开销 |
| **环境隔离** | ❌ 无 | ✅ 有 |
| **依赖管理** | ⭐⭐ 需要 Python | ⭐⭐⭐ 自动安装 |
| **跨平台** | ❌ Linux only | ✅ 所有平台 |
| **启动速度** | ⭐⭐⭐ 快 | ⭐⭐ 首次慢 |
| **推荐场景** | 生产环境 | 开发/测试 |

---

## 当前状态

**Webhook Server**: 运行在 Docker 容器内（42.194.162.251:5001）

**问题**: 容器内无法调用宿主机的 `openhands` 命令

**建议**: 使用方案 1（宿主机模式）重新部署

---

## 迁移步骤（从 Docker 到宿主机）

### 1. 停止 Docker 容器
```bash
docker stop openhands-webhook-server
docker rm openhands-webhook-server
```

### 2. 部署宿主机版本
```bash
cd webhook-deploy
export WEBHOOK_SECRET="your-secret"
./deploy-host.sh
```

### 3. 验证
```bash
curl http://127.0.0.1:5001/health
```

### 4. 测试
创建新的测试 issue，检查是否能正常调用 `openhands` 命令。

---

**更新日期**: 2026-03-07  
**版本**: v2.0
