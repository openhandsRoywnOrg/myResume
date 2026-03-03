# 🤖 AI DevOps 面试库

> 专业的 AI 运维开发面试知识总结网站 - 从基础到进阶的完整学习路径

[![Status](https://img.shields.io/badge/status-active%20development-brightgreen)](https://github.com/openhandsRoywnOrg/myResume)
[![Python](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-3.0-green)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

---

## 📖 项目简介

**AI DevOps 面试库** 是一个专业的面试知识总结网站，专注于 AI 运维开发（AI Ops / MLOps）领域。提供系统化的知识点、面试题库、学习路线和实战指南。

### ✨ 核心特性

- 📚 **知识点管理** - 系统化的知识分类和详细解析
- 🗺️ **知识地图** - 思维导图、技术路线、全景图
- 🤖 **AI 应用开发** - LangChain、LangGraph、MCP、Agent 协同
- 📐 **AI 软件工程** - 文档驱动、测试驱动、需求驱动
- 🔍 **全文搜索** - 快速定位知识点
- 📱 **响应式设计** - 桌面端和移动端完美适配

---

## 🎯 学习路径

### 💻 技术基础
- 🐧 **Linux** - 基础命令、网络配置、系统管理
- 🐳 **Docker** - 容器技术、Docker Compose
- ☸️ **Kubernetes** - 容器编排、服务部署

### 🤖 AI 应用开发
- 🦜 **LangChain** - LLM 应用开发框架
- 🕸️ **LangGraph** - 状态化 Agent 工作流
- 🔌 **MCP** - Model Context Protocol
- 🤝 **Agent 协同** - 多 Agent 协作与编排

### 📐 AI 软件工程
- 📄 **文档驱动开发** - DDD 与文档先行
- ✅ **测试驱动开发** - TDD 与自动化测试
- 🎯 **需求驱动开发** - 需求分析与拆解
- 🔄 **工程流程** - AI 工程化全流程

### 🗺️ 知识地图
- 🧠 **思维导图** - 可视化知识结构
- 🛣️ **技术路线** - 5 阶段学习路径
- 🌐 **AI DevOps 全景图** - 完整架构视图

---

## 🚀 快速开始

### 环境要求
- Python 3.12+
- Flask 3.0+

### 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/openhandsRoywnOrg/myResume.git
cd myResume

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行应用
cd ai-ops-interview
python app.py
```

### 访问应用
打开浏览器访问：`http://localhost:51880`

---

## 📁 项目结构

```
myResume/
├── ai-ops-interview/          # 前端应用
│   ├── app.py                 # Flask 主应用
│   ├── templates/             # HTML 模板
│   │   ├── index.html        # 首页
│   │   ├── mindmap.html      # 思维导图
│   │   ├── langchain.html    # LangChain 页面
│   │   ├── doc_driven.html   # 文档驱动开发
│   │   ├── tech_roadmap.html # 技术路线
│   │   └── ...
│   ├── static/css/
│   │   └── style.css         # 样式文件
│   └── content/              # Markdown 内容
│       ├── linux/
│       ├── docker/
│       ├── k8s/
│       └── ...
│
├── backend/                   # 后端服务
│   ├── app/
│   │   ├── models/           # 数据模型
│   │   ├── api/              # API 路由
│   │   ├── hooks/            # 钩子系统
│   │   └── services/         # 业务逻辑
│   └── tests/                # 测试代码
│
├── docs/                      # 项目文档
│   ├── PROJECT_PROGRESS.md   # 项目进展
│   ├── ARCHITECTURE_PLAN.md  # 架构设计
│   ├── AGENTS.md             # 开发指南
│   └── ...
│
└── .github/                   # GitHub 配置
    ├── workflows/            # CI/CD
    └── ISSUE_TEMPLATE/       # Issue 模板
```

---

## 📊 项目进展

### 已完成 ✅
- ✅ 知识点展示系统
- ✅ 全文搜索功能
- ✅ 思维导图可视化
- ✅ 统一导航栏（4 个主菜单，宽版下拉）
- ✅ 知识地图（技术路线、全景图）
- ✅ 权限系统（RBAC 模型）
- ✅ 响应式设计

### 进行中 🚧
- 🚧 后端服务集成
- 🚧 数据库实现
- 🚧 用户系统

### 计划中 📋
- 📋 面试题库管理
- 📋 AI 模拟面试
- 📋 智能评分系统
- 📋 学习进度追踪

详细进展请查看：[项目进展报告](docs/PROJECT_PROGRESS.md)

---

## 🎨 界面预览

### 导航栏
- **4 个主菜单**: 技术基础、AI 应用开发、AI 软件工程、知识地图
- **宽版下拉**: 600px 宽度，分栏布局
- **图标 + 描述**: 直观的菜单项

### 核心页面
- **首页**: 知识分类、快速搜索、功能介绍
- **思维导图**: 可视化知识结构
- **技术路线**: 5 阶段学习路径
- **全景图**: AI DevOps 完整架构

---

## 🧪 测试

### 运行测试
```bash
# 后端测试
cd backend
python -m pytest tests/ -v

# 权限测试
python test_permissions_simple.py
```

### 测试覆盖
- 用户模型：97%
- 认证装饰器：通过
- 数据库操作：通过

详细测试报告：[权限测试报告](docs/PERMISSION_TEST_REPORT.md)

---

## 📖 文档

| 文档 | 说明 |
|------|------|
| [项目进展](docs/PROJECT_PROGRESS.md) | 当前开发状态和里程碑 |
| [架构设计](ARCHITECTURE_PLAN.md) | 项目架构和重构方案 |
| [开发指南](AGENTS.md) | AI Agent 开发规范 |
| [Issue 指南](docs/ISSUE_GUIDELINES.md) | Issue 解决流程 |
| [权限测试](docs/PERMISSION_TEST_REPORT.md) | 权限系统测试报告 |

---

## 🤝 贡献指南

### 如何参与
1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 开发规范
- 查看 [AGENTS.md](AGENTS.md) 了解代码规范
- 查看 [ISSUE_GUIDELINES.md](docs/ISSUE_GUIDELINES.md) 了解 Issue 流程
- 所有代码变更需要包含测试
- 遵循项目架构设计

---

## 🛠️ 技术栈

- **前端**: HTML5, CSS3, JavaScript
- **后端**: Python 3.12, Flask 3.0
- **数据库**: SQLite (开发), PostgreSQL (计划)
- **认证**: JWT
- **部署**: Vercel
- **测试**: pytest

---

## 📄 开源协议

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 📞 联系方式

- **GitHub**: [openhandsRoywnOrg/myResume](https://github.com/openhandsRoywnOrg/myResume)
- **问题反馈**: 创建 [Issue](https://github.com/openhandsRoywnOrg/myResume/issues)
- **项目状态**: 🟢 活跃开发中

---

## 🙏 致谢

- 参照 [面试导航](https://www.mianshiya.com/) 风格设计
- 感谢所有贡献者

---

**Made with ❤️ by OpenHands Team**
