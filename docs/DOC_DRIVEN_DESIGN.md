# 📄 文档驱动开发页面设计规范

**参考**: Code Wiki (https://codewiki.google/github.com/modelcontextprotocol/python-sdk)  
**版本**: 1.0  
**创建日期**: 2025-03-03  
**状态**: 设计阶段

---

## 🎯 设计目标

基于 Code Wiki 的页面布局优势，为 AI DevOps Pro 的文档驱动开发页面设计现代化、专业的用户界面。

### 核心改进点

1. **左侧树状导航** - 清晰的知识点层级结构
2. **右侧目录导航** - "On this page" 快速跳转
3. **章节锚点链接** - 每个标题旁带 link 图标
4. **代码源码跳转** - 代码中的术语可跳转到相关知识点
5. **交互式图表** - 支持缩放的架构图
6. **AI 辅助入口** - 右下角提问功能
7. **更新时间显示** - 增加内容可信度

---

## 📐 页面布局

### 整体布局结构

```
┌─────────────────────────────────────────────────────────────────┐
│  Header (全局导航栏)                                            │
│  [Logo] AI DevOps Pro  [搜索框]              [🌙] [🔗] [🤖]    │
├──────────┬──────────────────────────────────────┬──────────────┤
│          │                                      │              │
│  左侧    │           主内容区域                  │   右侧       │
│  树状    │                                      │   目录       │
│  导航    │  # 文档驱动开发                       │   On this    │
│          │                                      │   page       │
│  📄 DDD  │  文档驱动开发是一种以文档为核心的...  │              │
│  ├─ 概述 │                                      │  ## 什么是   │
│  ├─ 原则 │  ## 什么是文档驱动开发？              │  ## 核心原则 │
│  ├─ 流程 │  ## 核心原则                        │  ## 开发流程 │
│  └─ 模板 │  ## 开发流程                        │  ## 文档模板 │
│          │  ## 文档模板                        │              │
│          │  ## AI 辅助工具                      │              │
│          │  ## 面试问题                        │              │
│          │                                      │              │
│          │  [← 返回首页] [下一个：TDD →]        │              │
│          │                                      │              │
├──────────┴──────────────────────────────────────┴──────────────┤
│  Footer                                                         │
│  AI DevOps Pro - Master the Skills. Land the Job.              │
└─────────────────────────────────────────────────────────────────┘
```

### 布局尺寸规范

```css
/* 容器布局 */
.layout-container {
  display: grid;
  grid-template-columns: 280px 1fr 240px; /* 左 - 中-右 */
  grid-template-rows: 64px 1fr auto;      /* header -内容-footer */
  min-height: 100vh;
}

/* 响应式断点 */
@media (max-width: 1200px) {
  .layout-container {
    grid-template-columns: 240px 1fr; /* 隐藏右侧目录 */
  }
  .right-sidebar { display: none; }
}

@media (max-width: 768px) {
  .layout-container {
    grid-template-columns: 1fr; /* 单栏布局 */
  }
  .left-sidebar { display: none; } /* 改为汉堡菜单 */
}
```

---

## 🧩 组件设计

### 1. 全局导航栏 (Global Header)

**参考**: Code Wiki 顶部导航

```html
<header class="global-header">
  <div class="header-left">
    <a href="/" class="logo-link">
      <span class="logo-icon">🤖⚙️</span>
      <span class="logo-text">AI DevOps Pro</span>
    </a>
  </div>
  
  <div class="header-center">
    <div class="search-box">
      <input 
        type="text" 
        placeholder="Search knowledge base..."
        class="search-input"
      >
      <button class="search-btn" aria-label="Search">
        <span class="icon">search</span>
      </button>
    </div>
  </div>
  
  <div class="header-right">
    <button class="theme-toggle" aria-label="Toggle theme">
      <span class="icon">dark_mode</span>
    </button>
    <button class="share-btn" aria-label="Share">
      <span class="icon">share</span>
    </button>
    <button class="ai-chat-btn" aria-label="AI Assistant">
      <span class="icon">spark</span>
      <span class="label">Chat</span>
    </button>
  </div>
</header>
```

**样式规范**:
```css
.global-header {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  background: var(--bg-primary);
  border-bottom: 1px solid var(--card-border);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.logo-link {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
  text-decoration: none;
}

.logo-icon {
  font-size: 28px;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--bg-secondary);
  border: 1px solid var(--card-border);
  border-radius: 8px;
  padding: 8px 16px;
  width: 400px;
}

.search-input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 14px;
  color: var(--text-primary);
}

.search-input::placeholder {
  color: var(--text-secondary);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-right button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.header-right button:hover {
  background: var(--bg-secondary);
  color: var(--text-primary);
}
```

---

### 2. 左侧树状导航 (Tree Navigation)

**参考**: Code Wiki 左侧目录树

```html
<aside class="left-sidebar">
  <nav class="tree-nav">
    <div class="nav-section">
      <div class="nav-section-header">
        <span class="section-icon">📄</span>
        <span class="section-title">文档驱动开发</span>
      </div>
      <ul class="nav-tree">
        <li class="tree-node">
          <button class="node-toggle" aria-expanded="true">
            <span class="arrow">▼</span>
          </button>
          <a href="#overview" class="node-link active">
            <span class="node-icon">📖</span>
            <span class="node-label">概述</span>
          </a>
        </li>
        <li class="tree-node">
          <button class="node-toggle" aria-expanded="true">
            <span class="arrow">▼</span>
          </button>
          <a href="#principles" class="node-link">
            <span class="node-icon">🎯</span>
            <span class="node-label">核心原则</span>
          </a>
        </li>
        <li class="tree-node">
          <button class="node-toggle" aria-expanded="false">
            <span class="arrow">▶</span>
          </button>
          <a href="#workflow" class="node-link">
            <span class="node-icon">🔄</span>
            <span class="node-label">开发流程</span>
          </a>
          <ul class="nav-tree-sub">
            <li class="tree-node-sub">
              <a href="#step-1">需求分析</a>
            </li>
            <li class="tree-node-sub">
              <a href="#step-2">文档设计</a>
            </li>
            <li class="tree-node-sub">
              <a href="#step-3">AI 生成</a>
            </li>
          </ul>
        </li>
        <li class="tree-node">
          <a href="#templates" class="node-link">
            <span class="node-icon">📋</span>
            <span class="node-label">文档模板</span>
          </a>
        </li>
        <li class="tree-node">
          <a href="#tools" class="node-link">
            <span class="node-icon">💡</span>
            <span class="node-label">AI 辅助工具</span>
          </a>
        </li>
        <li class="tree-node">
          <a href="#interview" class="node-link">
            <span class="node-icon">❓</span>
            <span class="node-label">面试问题</span>
          </a>
        </li>
      </ul>
    </div>
  </nav>
</aside>
```

**样式规范**:
```css
.left-sidebar {
  width: 280px;
  background: var(--bg-secondary);
  border-right: 1px solid var(--card-border);
  overflow-y: auto;
  padding: 24px 0;
}

.tree-nav {
  font-size: 14px;
}

.nav-section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  font-weight: 600;
  color: var(--text-primary);
  text-transform: uppercase;
  font-size: 12px;
  letter-spacing: 0.5px;
}

.nav-tree {
  list-style: none;
  padding: 0;
  margin: 0;
}

.tree-node {
  position: relative;
}

.node-toggle {
  position: absolute;
  left: 8px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  border: none;
  background: transparent;
  cursor: pointer;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
}

.node-link {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 24px 10px 40px;
  color: var(--text-secondary);
  text-decoration: none;
  transition: all 0.2s;
}

.node-link:hover {
  background: var(--card-bg);
  color: var(--text-primary);
}

.node-link.active {
  background: var(--primary-color);
  color: white;
}

.node-icon {
  font-size: 16px;
}

.nav-tree-sub {
  list-style: none;
  padding-left: 20px;
}

.tree-node-sub a {
  display: block;
  padding: 8px 24px;
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 13px;
}

.tree-node-sub a:hover {
  color: var(--primary-color);
}
```

---

### 3. 右侧目录导航 (Table of Contents)

**参考**: Code Wiki "On this page"

```html
<aside class="right-sidebar">
  <div class="toc-container">
    <div class="toc-header">
      <span class="toc-title">On this page</span>
    </div>
    <nav class="toc-nav">
      <ul class="toc-list">
        <li class="toc-item">
          <a href="#what-is-ddd" class="toc-link">
            <span class="link-icon">📖</span>
            <span>什么是文档驱动开发？</span>
          </a>
        </li>
        <li class="toc-item">
          <a href="#core-principles" class="toc-link">
            <span class="link-icon">🎯</span>
            <span>核心原则</span>
          </a>
        </li>
        <li class="toc-item">
          <a href="#workflow" class="toc-link">
            <span class="link-icon">🔄</span>
            <span>开发流程</span>
          </a>
        </li>
        <li class="toc-item">
          <a href="#templates" class="toc-link">
            <span class="link-icon">📋</span>
            <span>文档模板</span>
          </a>
        </li>
        <li class="toc-item">
          <a href="#ai-tools" class="toc-link">
            <span class="link-icon">💡</span>
            <span>AI 辅助工具</span>
          </a>
        </li>
        <li class="toc-item">
          <a href="#interview-questions" class="toc-link">
            <span class="link-icon">❓</span>
            <span>面试问题</span>
          </a>
        </li>
      </ul>
    </nav>
  </div>
</aside>
```

**样式规范**:
```css
.right-sidebar {
  width: 240px;
  padding: 24px 16px;
  border-left: 1px solid var(--card-border);
  overflow-y: auto;
  position: sticky;
  top: 64px;
  max-height: calc(100vh - 64px);
}

.toc-container {
  font-size: 13px;
}

.toc-header {
  padding: 8px 12px;
  font-weight: 600;
  color: var(--text-primary);
  text-transform: uppercase;
  font-size: 11px;
  letter-spacing: 0.5px;
}

.toc-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.toc-item {
  margin: 4px 0;
}

.toc-link {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  color: var(--text-secondary);
  text-decoration: none;
  border-radius: 6px;
  transition: all 0.2s;
}

.toc-link:hover {
  background: var(--bg-secondary);
  color: var(--text-primary);
}

.toc-link.active {
  background: var(--bg-secondary);
  color: var(--primary-color);
  font-weight: 500;
}

.link-icon {
  font-size: 14px;
  opacity: 0.7;
}
```

---

### 4. 主内容区域 (Main Content)

**章节标题设计**:

```html
<main class="main-content">
  <article class="content-article">
    <header class="article-header">
      <h1>📄 文档驱动开发 (DDD)</h1>
      <p class="subtitle">Document-Driven Development in AI Era</p>
      <div class="meta-info">
        <span class="update-time">
          <span class="icon">update</span>
          Last updated: 2025-03-03
        </span>
        <span class="commit-hash">
          <span class="icon">code</span>
          Based on commit <a href="#">abc123</a>
        </span>
      </div>
    </header>
    
    <section id="what-is-ddd" class="content-section">
      <h2>
        <a href="#what-is-ddd" class="anchor-link">
          <span class="icon">link</span>
        </a>
        📖 什么是文档驱动开发？
      </h2>
      <p>文档驱动开发是一种以文档为核心的软件开发方法论...</p>
    </section>
    
    <section id="core-principles" class="content-section">
      <h2>
        <a href="#core-principles" class="anchor-link">
          <span class="icon">link</span>
        </a>
        🎯 核心原则
      </h2>
      <!-- 内容 -->
    </section>
  </article>
</main>
```

**样式规范**:
```css
.main-content {
  padding: 48px 64px;
  max-width: 100%;
  overflow-x: hidden;
}

.content-article {
  max-width: 900px;
  margin: 0 auto;
  line-height: 1.8;
}

.article-header {
  margin-bottom: 48px;
  padding-bottom: 24px;
  border-bottom: 2px solid var(--card-border);
}

.article-header h1 {
  font-size: 42px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 16px 0;
  line-height: 1.2;
}

.article-header .subtitle {
  font-size: 20px;
  color: var(--text-secondary);
  margin: 0 0 16px 0;
  font-weight: 400;
}

.meta-info {
  display: flex;
  gap: 24px;
  font-size: 13px;
  color: var(--text-secondary);
}

.meta-info .icon {
  font-size: 14px;
  margin-right: 4px;
}

.content-section {
  margin: 48px 0;
  scroll-margin-top: 24px;
}

.content-section h2 {
  font-size: 28px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 24px 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.anchor-link {
  opacity: 0;
  color: var(--primary-color);
  text-decoration: none;
  transition: opacity 0.2s;
}

.content-section h2:hover .anchor-link {
  opacity: 1;
}

.content-section p {
  font-size: 16px;
  color: var(--text-primary);
  margin: 0 0 16px 0;
}
```

---

### 5. 代码块增强 (Enhanced Code Blocks)

**参考**: Code Wiki 代码跳转功能

```html
<div class="code-block-wrapper">
  <div class="code-header">
    <span class="code-language">python</span>
    <a href="https://github.com/your-repo/backend/app/models/topic.py" 
       class="source-link" 
       target="_blank">
      <span class="icon">code</span>
      View source
    </a>
  </div>
  <pre class="code-block"><code class="language-python">
<span class="keyword">from</span> <span class="module" data-link="/topics/pydantic">pydantic</span> <span class="keyword">import</span> BaseModel

<span class="keyword">class</span> <span class="class-name" data-link="/topics/base-model">Topic</span>(BaseModel):
    <span class="attr">id</span>: <span class="type" data-link="/topics/int">int</span>
    <span class="attr">title</span>: <span class="type" data-link="/topics/str">str</span>
    <span class="attr">content</span>: <span class="type" data-link="/topics/str">str</span>
  </code></pre>
</div>
```

**样式规范**:
```css
.code-block-wrapper {
  margin: 24px 0;
  border: 1px solid var(--card-border);
  border-radius: 8px;
  overflow: hidden;
}

.code-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 16px;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--card-border);
}

.code-language {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
}

.source-link {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--primary-color);
  text-decoration: none;
}

.source-link:hover {
  text-decoration: underline;
}

.code-block {
  padding: 16px;
  background: var(--bg-primary);
  overflow-x: auto;
  font-family: var(--font-mono);
  font-size: 14px;
  line-height: 1.6;
}

.code-block code [data-link] {
  color: var(--primary-color);
  cursor: pointer;
  text-decoration: underline;
  text-decoration-style: dotted;
}

.code-block code [data-link]:hover {
  background: var(--primary-color);
  color: white;
}
```

---

### 6. 交互式图表 (Interactive Diagrams)

**参考**: Code Wiki 架构图展示

```html
<div class="diagram-container">
  <div class="diagram-header">
    <span class="diagram-title">文档驱动开发流程图</span>
    <button class="zoom-btn" aria-label="Zoom">
      <span class="icon">zoom_in</span>
    </button>
  </div>
  <div class="diagram-content">
    <svg viewBox="0 0 800 400" class="interactive-diagram">
      <!-- 流程图内容 -->
      <g class="diagram-node" data-step="1">
        <rect x="50" y="150" width="120" height="80" rx="8"/>
        <text x="110" y="190" text-anchor="middle">需求分析</text>
      </g>
      <g class="diagram-arrow">
        <path d="M170 190 L220 190" marker-end="url(#arrowhead)"/>
      </g>
      <!-- 更多节点... -->
    </svg>
  </div>
  <div class="diagram-footer">
    <span class="diagram-caption">图 1: 文档驱动开发的五个核心步骤</span>
  </div>
</div>
```

**样式规范**:
```css
.diagram-container {
  margin: 32px 0;
  border: 1px solid var(--card-border);
  border-radius: 8px;
  overflow: hidden;
}

.diagram-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--card-border);
}

.diagram-title {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 14px;
}

.zoom-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  border-radius: 4px;
}

.zoom-btn:hover {
  background: var(--card-border);
}

.diagram-content {
  padding: 24px;
  background: var(--card-bg);
  overflow: auto;
}

.interactive-diagram {
  width: 100%;
  height: auto;
  cursor: grab;
}

.interactive-diagram:active {
  cursor: grabbing;
}

.diagram-footer {
  padding: 12px 16px;
  background: var(--bg-secondary);
  border-top: 1px solid var(--card-border);
}

.diagram-caption {
  font-size: 13px;
  color: var(--text-secondary);
  font-style: italic;
}
```

---

### 7. AI 辅助入口 (AI Assistant Widget)

**参考**: Code Wiki 右下角聊天入口

```html
<div class="ai-assistant-widget">
  <button class="ai-chat-toggle" aria-label="Ask AI">
    <span class="icon">spark</span>
    <span class="badge">3</span>
  </button>
  
  <div class="ai-chat-panel">
    <div class="chat-header">
      <h3>AI Assistant</h3>
      <button class="close-btn">×</button>
    </div>
    <div class="chat-body">
      <div class="chat-message ai">
        <p>Hi! I can help you understand Document-Driven Development. What would you like to know?</p>
      </div>
    </div>
    <div class="chat-input">
      <input 
        type="text" 
        placeholder="Ask about this topic..."
        class="chat-input-field"
      >
      <button class="send-btn">
        <span class="icon">send</span>
      </button>
    </div>
  </div>
</div>
```

**样式规范**:
```css
.ai-assistant-widget {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 2000;
}

.ai-chat-toggle {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  border: none;
  background: var(--primary-gradient);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  transition: transform 0.2s, box-shadow 0.2s;
  position: relative;
}

.ai-chat-toggle:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.5);
}

.ai-chat-toggle .icon {
  font-size: 24px;
}

.badge {
  position: absolute;
  top: -4px;
  right: -4px;
  background: #ff4757;
  color: white;
  font-size: 12px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 10px;
}

.ai-chat-panel {
  position: absolute;
  bottom: 72px;
  right: 0;
  width: 360px;
  height: 500px;
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid var(--card-border);
}

.chat-header h3 {
  margin: 0;
  font-size: 16px;
  color: var(--text-primary);
}

.close-btn {
  border: none;
  background: transparent;
  font-size: 24px;
  color: var(--text-secondary);
  cursor: pointer;
}

.chat-body {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}

.chat-message {
  margin: 12px 0;
  padding: 12px 16px;
  border-radius: 12px;
  max-width: 80%;
}

.chat-message.ai {
  background: var(--bg-secondary);
  color: var(--text-primary);
}

.chat-input {
  display: flex;
  gap: 8px;
  padding: 16px;
  border-top: 1px solid var(--card-border);
}

.chat-input-field {
  flex: 1;
  padding: 10px 14px;
  border: 1px solid var(--card-border);
  border-radius: 8px;
  font-size: 14px;
}

.send-btn {
  width: 40px;
  height: 40px;
  border: none;
  background: var(--primary-color);
  color: white;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
```

---

## 🎨 主题系统

### CSS 变量定义

```css
:root {
  /* 主色调 */
  --primary-color: #667eea;
  --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --secondary-color: #764ba2;
  --accent-color: #f093fb;
  
  /* 浅色主题 */
  --bg-primary: #ffffff;
  --bg-secondary: #f8f9fa;
  --card-bg: #ffffff;
  --text-primary: #1a1a2e;
  --text-secondary: #4a4a68;
  --card-border: #e8e8f0;
  
  /* 字体 */
  --font-primary: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-heading: 'Inter', -apple-system, sans-serif;
  --font-mono: 'Fira Code', 'Monaco', monospace;
  
  /* 间距 */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-2xl: 48px;
  
  /* 圆角 */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  
  /* 阴影 */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.12);
}

/* 深色主题 */
[data-theme="dark"] {
  --bg-primary: #0f0f1a;
  --bg-secondary: #1a1a2e;
  --card-bg: #1a1a2e;
  --text-primary: #ffffff;
  --text-secondary: #b8b8d0;
  --card-border: #2a2a3e;
}
```

---

## 📱 响应式设计

### 断点定义

```css
/* Mobile: < 768px */
@media (max-width: 767px) {
  .layout-container {
    grid-template-columns: 1fr;
  }
  
  .left-sidebar,
  .right-sidebar {
    display: none;
  }
  
  .main-content {
    padding: 24px 16px;
  }
  
  .article-header h1 {
    font-size: 28px;
  }
}

/* Tablet: 768px - 1199px */
@media (min-width: 768px) and (max-width: 1199px) {
  .layout-container {
    grid-template-columns: 240px 1fr;
  }
  
  .right-sidebar {
    display: none;
  }
  
  .main-content {
    padding: 32px 40px;
  }
}

/* Desktop: >= 1200px */
@media (min-width: 1200px) {
  .layout-container {
    grid-template-columns: 280px 1fr 240px;
  }
}
```

---

## 🎯 交互规范

### 1. 滚动行为

```javascript
// 平滑滚动到锚点
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});

// 右侧目录高亮当前章节
const observer = new IntersectionObserver(
  entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.id;
        document.querySelectorAll('.toc-link').forEach(link => {
          link.classList.remove('active');
          if (link.getAttribute('href') === `#${id}`) {
            link.classList.add('active');
          }
        });
      }
    });
  },
  { rootMargin: '-100px 0px -60% 0px' }
);

document.querySelectorAll('.content-section').forEach(section => {
  observer.observe(section);
});
```

### 2. 树状导航折叠

```javascript
// 树节点折叠/展开
document.querySelectorAll('.node-toggle').forEach(toggle => {
  toggle.addEventListener('click', function() {
    const arrow = this.querySelector('.arrow');
    const isExpanded = this.getAttribute('aria-expanded') === 'true';
    
    this.setAttribute('aria-expanded', !isExpanded);
    arrow.textContent = isExpanded ? '▶' : '▼';
    
    const subTree = this.parentElement.querySelector('.nav-tree-sub');
    if (subTree) {
      subTree.style.display = isExpanded ? 'none' : 'block';
    }
  });
});
```

### 3. 主题切换

```javascript
// 主题切换
const themeToggle = document.querySelector('.theme-toggle');
themeToggle.addEventListener('click', function() {
  const currentTheme = document.documentElement.getAttribute('data-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  
  document.documentElement.setAttribute('data-theme', newTheme);
  localStorage.setItem('theme', newTheme);
  
  this.querySelector('.icon').textContent = 
    newTheme === 'dark' ? 'light_mode' : 'dark_mode';
});

// 初始化主题
const savedTheme = localStorage.getItem('theme') || 'light';
document.documentElement.setAttribute('data-theme', savedTheme);
```

---

## ✅ 验收标准

### 视觉验收

- [ ] 三栏布局在桌面端正常显示
- [ ] 左侧树状导航支持折叠/展开
- [ ] 右侧目录随滚动自动高亮
- [ ] 章节标题悬停显示锚点链接
- [ ] 代码块支持跳转到源码
- [ ] 图表支持缩放操作
- [ ] AI 助手按钮固定在右下角
- [ ] 深色/浅色主题切换正常

### 功能验收

- [ ] 点击左侧导航平滑滚动到对应章节
- [ ] 点击右侧目录平滑滚动到对应章节
- [ ] 树状导航状态持久化（可选）
- [ ] 主题偏好持久化
- [ ] 移动端导航自动隐藏
- [ ] 所有交互有平滑动画

### 性能验收

- [ ] 首屏加载时间 < 2 秒
- [ ] 滚动无卡顿
- [ ] 动画帧率 > 60fps
- [ ] 移动端触控响应 < 100ms

---

## 📚 参考资料

- **Code Wiki**: https://codewiki.google/
- **Material Design Icons**: https://fonts.google.com/icons
- **Inter Font**: https://rsms.me/inter/
- **Fira Code**: https://github.com/tonsky/FiraCode

---

**维护者**: AI DevOps Pro Team  
**最后更新**: 2025-03-03  
**下次审查**: 2025-03-10
