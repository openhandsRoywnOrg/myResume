
# Linux 基础

## 概述

Linux 是一个开源的类 Unix 操作系统，广泛应用于服务器、云计算和嵌入式系统。

## 核心概念

### 1. 文件系统结构

Linux 采用树状文件系统结构：

- `/` - 根目录
- `/home` - 用户主目录
- `/etc` - 配置文件
- `/var` - 可变数据
- `/usr` - 用户程序
- `/bin` - 基本命令
- `/sbin` - 系统管理命令

### 2. 常用命令

```bash
# 文件和目录操作
ls -la          # 列出目录内容
cd /path        # 切换目录
pwd             # 显示当前路径
mkdir dir       # 创建目录
rm -rf dir      # 删除目录

# 文件查看
cat file        # 查看文件内容
less file       # 分页查看
tail -f file    # 实时查看日志

# 权限管理
chmod 755 file  # 修改权限
chown user file # 修改所有者
```

### 3. 进程管理

```bash
ps aux          # 查看进程
top             # 动态查看进程
kill PID        # 终止进程
systemctl status service  # 查看服务状态
```

## 面试常见问题

1. **Linux 权限系统是如何工作的？**
   - 读 (r)=4, 写 (w)=2, 执行 (x)=1
   - 权限分为所有者、组、其他用户

2. **如何查看系统资源使用情况？**
   - 使用 `top`, `htop`, `free -m`, `df -h` 等命令

3. **什么是 inode？**
   - inode 是文件系统中存储文件元数据的数据结构

