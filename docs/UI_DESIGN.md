# 🎨 AI DevOps 知识库 - UI 设计方案

**设计灵感**: Code Wiki (https://codewiki.google/)  
**设计风格**: 极简主义 + 卡片式布局 + 可视化数据  
**更新日期**: 2025-03-03

---

## 🎯 设计理念

### 核心原则
1. **极简主义** - 干净的布局，大量留白，聚焦内容
2. **卡片式布局** - 模块化展示，易于维护
3. **可视化数据** - 学习进度、技术栈用图表展示
4. **动态更新** - 自动反映学习进展
5. **深色/浅色主题** - 用户可选

### 色彩方案

#### 主色调
```css
--primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
--primary-color: #667eea;
--secondary-color: #764ba2;
```

#### 浅色主题
```css
--bg-primary: #ffffff;
--bg-secondary: #f8f9fa;
--text-primary: #1a1a2e;
--text-secondary: #4a4a68;
--border-color: #e8e8f0;
```

#### 深色主题
```css
--bg-primary: #0f0f1a;
--bg-secondary: #1a1a2e;
--text-primary: #ffffff;
--text-secondary: #b8b8d0;
--border-color: #2a2a3e;
```

---

## 📐 页面布局

### 1. 首页设计

```
┌─────────────────────────────────────────────────────────────┐
│  [Logo] AI DevOps 知识库              [搜索框]    [🌙主题]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  💻 技术基础  🤖 AI 应用  📐 AI 工程  🗺️ 知识地图          │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  # 你好，我是 [姓名]                                        │
│  AI DevOps 工程师 | 持续学习者                              │
│                                                             │
│  [查看简历 ↓]  [联系我也 ↓]                                 │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ## 🛠️ 技术栈                                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │ 💻 Linux │ │ 🐳 Docker│ │ ☸️ K8s   │ │ 🤖 AI    │      │
│  │  ★★★★☆  │ │  ★★★★☆  │ │  ★★★☆☆  │ │  ★★☆☆☆  │      │
│  │  80%     │ │  75%     │ │  60%     │ │  40%     │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ## 📈 学习进度                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  总进度 ████████████░░░░░░░░  65%                  │   │
│  │  阶段 1: 基础入门      ✅ 完成                      │   │
│  │  阶段 2: 运维开发核心  🔄 进行中                    │   │
│  │  阶段 3: AI/ML 基础    ⏳ 未开始                    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ## 📚 最近学习                                             │
│  ┌──────────────────┐ ┌──────────────────┐                │
│  │ 📄 Docker Compose│ │ 📄 Kubernetes    │                │
│  │ 2025-03-02       │ │ 2025-03-01       │                │
│  │ 多容器编排管理   │ │ 容器编排平台     │                │
│  └──────────────────┘ └──────────────────┘                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. 知识库页面

```
┌─────────────────────────────────────────────────────────────┐
│  导航栏（同上）                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  # 🤖 AI 应用开发                                           │
│  LLM 应用开发框架、Agent 协同、MCP 协议                     │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 🦜 LangChain                                        │   │
│  │ LLM 应用开发框架                                     │   │
│  │ ████████████████░░  80% 掌握                        │   │
│  │ [开始学习] [查看详情]                                │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 🕸️ LangGraph                                        │   │
│  │ 构建状态化 Agent 工作流                               │   │
│  │ ████████░░░░░░░░░░  40% 掌握                        │   │
│  │ [开始学习] [查看详情]                                │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3. 简历页面

```
┌─────────────────────────────────────────────────────────────┐
│  导航栏（同上）                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  # 📄 个人简历                                              │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ## 💼 工作经历                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 2023 - 至今     高级 DevOps 工程师    XXX 公司       │   │
│  │ • 负责 CI/CD 流程优化                                 │   │
│  │ • 搭建 Kubernetes 集群                               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ## 🎓 教育背景                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 2019 - 2023     计算机科学与技术    XXX 大学         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ## 📜 证书认证                                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                  │
│  │ CKA      │ │ AWS      │ │ GCP      │                  │
│  │ 2024     │ │ 2023     │ │ 2023     │                  │
│  └──────────┘ └──────────┘ └──────────┘                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4. 学习进度页面

```
┌─────────────────────────────────────────────────────────────┐
│  导航栏（同上）                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  # 📊 学习进度追踪                                          │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐  ┌─────────────────┐                 │
│  │   雷达图        │  │   时间轴        │                 │
│  │  技术栈能力     │  │  学习历程       │                 │
│  └─────────────────┘  └─────────────────┘                 │
│                                                             │
│  ## 阶段进度                                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 阶段 1: 基础入门                                     │   │
│  │ ████████████████████  100% ✅                       │   │
│  │ Linux | Docker | Git | Python                       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 阶段 2: 运维开发核心                                 │   │
│  │ ████████████░░░░░░░░  60% 🔄                        │   │
│  │ K8s | CI/CD | Monitoring                            │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧩 组件设计

### 1. 导航栏组件
```html
<nav class="navbar">
    <div class="nav-brand">
        <span class="logo">🚀</span>
        <span class="title">AI DevOps 知识库</span>
    </div>
    
    <div class="nav-search">
        <input type="text" placeholder="搜索知识点...">
        <button>🔍</button>
    </div>
    
    <div class="nav-menu">
        <!-- 4 个主菜单 -->
    </div>
    
    <button class="theme-toggle">🌙</button>
</nav>
```

### 2. 技术栈卡片
```html
<div class="tech-card">
    <div class="tech-icon">💻</div>
    <div class="tech-name">Linux</div>
    <div class="tech-level">
        <div class="stars">★★★★☆</div>
        <div class="progress-bar">
            <div class="progress" style="width: 80%"></div>
        </div>
        <div class="percentage">80%</div>
    </div>
</div>
```

### 3. 知识点卡片
```html
<div class="knowledge-card">
    <div class="card-header">
        <span class="icon">🦜</span>
        <h3>LangChain</h3>
    </div>
    <div class="card-body">
        <p>LLM 应用开发框架</p>
        <div class="mastery">
            <div class="progress-bar">
                <div class="progress" style="width: 80%"></div>
            </div>
            <span>80% 掌握</span>
        </div>
    </div>
    <div class="card-footer">
        <a href="#" class="btn-primary">开始学习</a>
        <a href="#" class="btn-secondary">查看详情</a>
    </div>
</div>
```

### 4. 进度追踪卡片
```html
<div class="progress-card">
    <div class="progress-header">
        <h4>阶段 1: 基础入门</h4>
        <span class="status completed">✅</span>
    </div>
    <div class="progress-bar">
        <div class="progress" style="width: 100%"></div>
    </div>
    <div class="progress-topics">
        <span class="topic">Linux</span>
        <span class="topic">Docker</span>
        <span class="topic">Git</span>
    </div>
</div>
```

---

## 🎭 交互设计

### 1. 悬停效果
```css
.tech-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(102, 126, 234, 0.2);
}

.knowledge-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
```

### 2. 加载动画
```css
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.card {
    animation: fadeIn 0.5s ease-out;
}
```

### 3. 进度条动画
```css
@keyframes progressFill {
    from { width: 0; }
}

.progress {
    animation: progressFill 1s ease-out;
}
```

---

## 📱 响应式设计

### 断点
```css
/* 移动端 */
@media (max-width: 768px) {
    .navbar { flex-direction: column; }
    .tech-grid { grid-template-columns: 1fr; }
    .knowledge-grid { grid-template-columns: 1fr; }
}

/* 平板端 */
@media (max-width: 1024px) {
    .tech-grid { grid-template-columns: repeat(2, 1fr); }
    .knowledge-grid { grid-template-columns: repeat(2, 1fr); }
}

/* 桌面端 */
@media (min-width: 1025px) {
    .tech-grid { grid-template-columns: repeat(4, 1fr); }
    .knowledge-grid { grid-template-columns: repeat(3, 1fr); }
}
```

---

## 🎨 主题切换

### 浅色主题
```css
:root[data-theme="light"] {
    --bg-primary: #ffffff;
    --bg-secondary: #f8f9fa;
    --text-primary: #1a1a2e;
    --text-secondary: #4a4a68;
    --card-bg: #ffffff;
    --card-shadow: rgba(0, 0, 0, 0.1);
}
```

### 深色主题
```css
:root[data-theme="dark"] {
    --bg-primary: #0f0f1a;
    --bg-secondary: #1a1a2e;
    --text-primary: #ffffff;
    --text-secondary: #b8b8d0;
    --card-bg: #1a1a2e;
    --card-shadow: rgba(0, 0, 0, 0.3);
}
```

---

## 📊 数据可视化

### 1. 雷达图（技术栈能力）
```javascript
// 使用 Chart.js 或类似库
const radarChart = new Chart(ctx, {
    type: 'radar',
    data: {
        labels: ['Linux', 'Docker', 'K8s', 'Python', 'AI/ML'],
        datasets: [{
            label: '当前水平',
            data: [80, 75, 60, 70, 40],
            backgroundColor: 'rgba(102, 126, 234, 0.2)',
            borderColor: '#667eea',
        }]
    }
});
```

### 2. 时间轴（学习历程）
```html
<div class="timeline">
    <div class="timeline-item completed">
        <div class="timeline-dot"></div>
        <div class="timeline-content">
            <h4>开始学习 Linux</h4>
            <p>2025-01-15</p>
        </div>
    </div>
    <div class="timeline-item current">
        <div class="timeline-dot"></div>
        <div class="timeline-content">
            <h4>学习 Docker</h4>
            <p>2025-03-01</p>
        </div>
    </div>
</div>
```

---

## 🚀 实施计划

### 第一阶段：基础样式（1-2 天）
- [ ] 更新全局 CSS 变量
- [ ] 实现主题切换
- [ ] 优化导航栏样式
- [ ] 创建卡片组件

### 第二阶段：首页重构（2-3 天）
- [ ] 设计个人简介区域
- [ ] 实现技术栈卡片
- [ ] 添加学习进度展示
- [ ] 创建最近学习列表

### 第三阶段：页面优化（3-4 天）
- [ ] 知识库页面卡片布局
- [ ] 简历页面时间轴
- [ ] 进度追踪图表
- [ ] 响应式适配

### 第四阶段：交互优化（2-3 天）
- [ ] 添加悬停效果
- [ ] 实现加载动画
- [ ] 进度条动画
- [ ] 平滑滚动

---

## 📝 注意事项

1. **保持简洁** - 不要过度设计，聚焦内容
2. **性能优先** - 避免过多的动画和特效
3. **可访问性** - 确保色盲用户也能使用
4. **一致性** - 保持设计语言统一
5. **移动端** - 优先保证移动端体验

---

**设计参考**:
- Code Wiki: https://codewiki.google/
- Dribbble: 搜索 "Dashboard UI"
- Material Design: https://material.io/

**维护者**: OpenHands Team  
**最后更新**: 2025-03-03
