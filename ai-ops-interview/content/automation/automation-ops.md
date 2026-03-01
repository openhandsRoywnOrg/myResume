
# 自动化运维

## 1. 自动化运维概述

自动化运维（Automation Ops）通过工具和脚本自动执行重复性运维任务，提高效率、减少人为错误。

### 核心价值：
- **效率提升**：快速执行重复任务
- **一致性**：消除人为差异
- **可追溯**：所有操作有记录
- **可扩展**：轻松管理大规模系统

## 2. Ansible 自动化

### 安装配置
```bash
pip install ansible
```

### Inventory 文件
```ini
# inventory.ini
[webservers]
web1.example.com
web2.example.com

[dbservers]
db1.example.com
db2.example.com

[ml-servers]
ml-worker-[1:5].example.com

[all:vars]
ansible_user=ubuntu
ansible_python_interpreter=/usr/bin/python3
```

### Playbook 示例
```yaml
# deploy-model.yml
---
- name: Deploy ML Model
  hosts: ml-servers
  become: yes
  vars:
    model_version: "v1.2.0"
    app_port: 8000

  tasks:
    - name: Install dependencies
      apt:
        name:
          - python3
          - python3-pip
          - docker.io
        state: present

    - name: Create application directory
      file:
        path: /opt/ml-service
        state: directory
        owner: ubuntu
        group: ubuntu

    - name: Copy model files
      copy:
        src: /path/to/model/
        dest: /opt/ml-service/model/

    - name: Install Python packages
      pip:
        requirements: /opt/ml-service/requirements.txt

    - name: Start service with systemd
      systemd:
        name: ml-service
        state: started
        enabled: yes
        daemon_reload: yes

    - name: Verify service is running
      uri:
        url: "http://localhost:{{ app_port }}/health"
        return_content: yes
      register: result
      retries: 5
      delay: 10
      until: result.status == 200
```

### 角色（Role）结构
```
roles/
├── ml-service/
│   ├── tasks/
│   │   └── main.yml
│   ├── handlers/
│   │   └── main.yml
│   ├── templates/
│   │   └── service.conf.j2
│   ├── files/
│   └── vars/
│       └── main.yml
```

## 3. Python 自动化脚本

### 批量服务器管理
```python
import paramiko
import json
from concurrent.futures import ThreadPoolExecutor

class ServerManager:
    def __init__(self, servers):
        self.servers = servers

    def execute_command(self, server, command):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(
                hostname=server['host'],
                username=server['username'],
                password=server['password'],
                port=server.get('port', 22)
            )

            stdin, stdout, stderr = ssh.exec_command(command)
            result = {
                'server': server['host'],
                'stdout': stdout.read().decode(),
                'stderr': stderr.read().decode(),
                'exit_code': stdout.channel.recv_exit_status()
            }

            return result
        finally:
            ssh.close()

    def execute_on_all(self, command, max_workers=10):
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(
                lambda s: self.execute_command(s, command),
                self.servers
            ))
        return results

    def deploy_model(self, model_path):
        commands = [
            f'mkdir -p /opt/models',
            f'rsync -avz {model_path} /opt/models/',
            f'systemctl restart ml-service'
        ]

        for cmd in commands:
            results = self.execute_on_all(cmd)
            for result in results:
                if result['exit_code'] != 0:
                    print(f"Error on {result['server']}: {result['stderr']}")

# 使用示例
servers = [
    {'host': 'ml1.example.com', 'username': 'ubuntu', 'password': 'xxx'},
    {'host': 'ml2.example.com', 'username': 'ubuntu', 'password': 'xxx'},
]

manager = ServerManager(servers)
manager.deploy_model('/path/to/model')
```

### 自动备份脚本
```python
import os
import subprocess
import boto3
from datetime import datetime

class BackupManager:
    def __init__(self, s3_bucket, retention_days=30):
        self.s3_bucket = s3_bucket
        self.retention_days = retention_days
        self.s3_client = boto3.client('s3')

    def backup_database(self, db_host, db_name, db_user):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f'{db_name}_{timestamp}.sql'

        # 执行数据库备份
        cmd = f'mysqldump -h {db_host} -u {db_user} -p {db_name} > /tmp/{backup_file}'
        subprocess.run(cmd, shell=True, check=True)

        # 压缩备份文件
        subprocess.run(f'gzip /tmp/{backup_file}', shell=True, check=True)

        # 上传到 S3
        compressed_file = f'/tmp/{backup_file}.gz'
        s3_key = f'backups/{db_name}/{backup_file}.gz'

        self.s3_client.upload_file(compressed_file, self.s3_bucket, s3_key)

        # 清理本地文件
        os.remove(compressed_file)

        return s3_key

    def cleanup_old_backups(self, prefix):
        cutoff_date = datetime.now().timestamp() - (self.retention_days * 86400)

        response = self.s3_client.list_objects_v2(
            Bucket=self.s3_bucket,
            Prefix=prefix
        )

        for obj in response.get('Contents', []):
            if obj['LastModified'].timestamp() < cutoff_date:
                self.s3_client.delete_object(
                    Bucket=self.s3_bucket,
                    Key=obj['Key']
                )
                print(f"Deleted old backup: {obj['Key']}")
```

## 4. 定时任务管理

### Cron 配置
```bash
# 编辑 crontab
crontab -e

# 示例配置
# 每天凌晨 2 点备份数据库
0 2 * * * /opt/scripts/backup.sh >> /var/log/backup.log 2>&1

# 每小时检查服务健康状态
0 * * * * /opt/scripts/health-check.sh

# 每周一清理 7 天前的日志
0 3 * * 1 find /var/log -name "*.log" -mtime +7 -delete
```

### Systemd Timer
```ini
# /etc/systemd/system/backup.timer
[Unit]
Description=Daily Backup Timer

[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

```ini
# /etc/systemd/system/backup.service
[Unit]
Description=Daily Backup Service

[Service]
Type=oneshot
ExecStart=/opt/scripts/backup.sh
```

```bash
# 启用定时器
systemctl enable backup.timer
systemctl start backup.timer

# 查看状态
systemctl list-timers
```

## 5. 配置管理

### 使用 Jinja2 模板
```python
from jinja2 import Template

# 定义模板
template_str = """
server {
    listen {{ port }};
    server_name {{ server_name }};

    location / {
        proxy_pass http://{{ backend_host }}:{{ backend_port }};
    }
}
"""

# 渲染配置
template = Template(template_str)
config = template.render(
    port=80,
    server_name='api.example.com',
    backend_host='localhost',
    backend_port=8000
)

# 写入配置文件
with open('/etc/nginx/conf.d/api.conf', 'w') as f:
    f.write(config)
```

### 配置版本控制
```python
import git
import hashlib

class ConfigManager:
    def __init__(self, repo_path):
        self.repo = git.Repo(repo_path)

    def save_config(self, config_path, description):
        # 计算配置哈希
        with open(config_path, 'rb') as f:
            config_hash = hashlib.md5(f.read()).hexdigest()

        # 添加到 git
        self.repo.index.add([config_path])
        self.repo.index.commit(f'{description} (hash: {config_hash})')

        # 推送到远程
        self.repo.remote().push()

        return config_hash

    def rollback(self, commit_hash):
        self.repo.git.reset('--hard', commit_hash)
        self.repo.remote().push('--force')
```

## 6. 自动扩缩容

### 基于指标的自动扩缩容
```python
import boto3

class AutoScaler:
    def __init__(self, asg_name, min_size=2, max_size=10):
        self.asg_name = asg_name
        self.min_size = min_size
        self.max_size = max_size
        self.autoscaling = boto3.client('autoscaling')
        self.cloudwatch = boto3.client('cloudwatch')

    def get_cpu_utilization(self):
        response = self.cloudwatch.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[{'Name': 'AutoScalingGroupName', 'Value': self.asg_name}],
            StartTime=datetime.utcnow() - timedelta(minutes=5),
            EndTime=datetime.utcnow(),
            Period=300,
            Statistics=['Average']
        )

        if response['Datapoints']:
            return response['Datapoints'][0]['Average']
        return 0

    def scale(self):
        cpu = self.get_cpu_utilization()

        # 获取当前容量
        response = self.autoscaling.describe_auto_scaling_groups(
            AutoScalingGroupNames=[self.asg_name]
        )
        current_capacity = response['AutoScalingGroups'][0]['DesiredCapacity']

        if cpu > 80 and current_capacity < self.max_size:
            # CPU 过高，扩容
            new_capacity = min(current_capacity + 2, self.max_size)
            self.autoscaling.set_desired_capacity(
                AutoScalingGroupName=self.asg_name,
                DesiredCapacity=new_capacity
            )
            print(f"Scaled up to {new_capacity}")

        elif cpu < 30 and current_capacity > self.min_size:
            # CPU 过低，缩容
            new_capacity = max(current_capacity - 1, self.min_size)
            self.autoscaling.set_desired_capacity(
                AutoScalingGroupName=self.asg_name,
                DesiredCapacity=new_capacity
            )
            print(f"Scaled down to {new_capacity}")
```

## 7. 健康检查与自愈

### 健康检查脚本
```python
import requests
import tim
|------|---------|------|
| DEBUG | 调试信息 | 变量值、中间结果 |
| INFO | 正常操作 | 服务启动、请求处理 |
| WARNING | 潜在问题 | 重试、降级 |
| ERROR | 错误但可恢复 | 单个请求失败 |
| CRITICAL | 严重错误 | 服务不可用 |

**最佳实践：**
- 生产环境使用 INFO 及以上
- 开发环境使用 DEBUG
- 错误日志必须包含堆栈跟踪
- 敏感信息需要脱敏

### Q4: 解释 APM（应用性能管理）

**答案：**

**APM**是监控和管理应用程序性能的系统。

**核心功能：**
1. **指标收集**：延迟、吞吐量、错误率
2. **分布式追踪**：请求链路追踪
3. **依赖映射**：服务依赖关系
4. **代码级分析**：性能瓶颈定位
5. **用户体验监控**：前端性能

**常用工具：**
- New Relic
- Datadog
- Dynatrace
- SkyWalking
- Pinpoint

### Q5: 如何实现日志的集中管理？

**答案：**

**架构方案：**

```
应用服务器 → Filebeat/Fluentd → Logstash → Elasticsearch → Kibana
                                    ↓
                              Alertmanager
```

**实施步骤：**

1. **日志收集：**
   - 使用 Filebeat 或 Fluentd
   - 配置日志路径和格式解析

2. **日志处理：**
   - Logstash 过滤和转换
   - 添加元数据（环境、服务名）

3. **日志存储：**
   - Elasticsearch 索引
   - 设置保留策略（如 30 天）

4. **日志查询：**
   - Kibana 搜索和可视化
   - 保存常用查询

5. **告警集成：**
   - 基于日志内容告警
   - 集成通知渠道
