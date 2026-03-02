
# Linux 网络配置

## 概述

Linux 网络配置是系统管理员必须掌握的核心技能之一。

## 网络命令

### 1. 网络接口查看

```bash
ip addr show        # 查看 IP 地址
ifconfig            # 传统命令（已废弃）
ip link show        # 查看网络接口状态
```

### 2. 网络连通性测试

```bash
ping google.com     # 测试连通性
traceroute host     # 跟踪路由
curl http://host    # HTTP 请求
wget url            # 下载文件
```

### 3. 端口和连接

```bash
netstat -tulpn      # 查看端口占用
ss -tulpn           # 新版替代命令
lsof -i :80         # 查看特定端口
```

### 4. 防火墙配置

```bash
# iptables
iptables -L -n -v
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# firewalld (CentOS/RHEL)
firewall-cmd --list-all
firewall-cmd --add-port=80/tcp --permanent

# ufw (Ubuntu)
ufw status
ufw allow 22/tcp
```

## DNS 配置

```bash
# 查看 DNS
cat /etc/resolv.conf

# 测试 DNS 解析
nslookup domain.com
dig domain.com
```

## 面试常见问题

1. **如何排查网络连接问题？**
   - 使用 ping 测试连通性
   - 使用 traceroute 查看路由
   - 检查防火墙规则
   - 查看 DNS 解析

2. **TCP 三次握手是什么？**
   - SYN -> SYN-ACK -> ACK

3. **如何查看某个端口被哪个进程占用？**
   - `netstat -tulpn | grep PORT`
   - `lsof -i :PORT`
   - `ss -tulpn | grep PORT`

