---
name: AI Agent 任务
description: 使用 @openhands-agent 自动解决任务
title: "[AI Task]: "
labels: ["ai-agent"]
body:
  - type: markdown
    attributes:
      value: |
        ## 📚 AI Agent 必读规范
        
        在开始编码前，**必须**阅读以下文档：
        
        ### 核心规范
        1. **[AGENTS.md](../AGENTS.md)** - AI 开发指南（⭐ 最重要）
           - 代码质量要求
           - 文件组织规则
           - Issue 解决流程
           - 常见错误示例
        
        2. **[ARCHITECTURE_PLAN.md](../ARCHITECTURE_PLAN.md)** - 架构设计
           - 项目目标架构
           - 目录结构说明
           - 分层设计原则
        
        3. **[backend/README.md](../backend/README.md)** - 后端目录结构
           - 模块职责说明
           - 添加新功能的流程
        
        4. **[docs/ISSUE_GUIDELINES.md](../docs/ISSUE_GUIDELINES.md)** - Issue 解决指南
           - 7 步解决流程
           - 代码规范示例
           - 测试编写指南
        
        ### ⚠️ 重要规则
        
        - ✅ **所有新代码必须有单元测试**（覆盖率 > 80%）
        - ✅ **遵循现有代码风格**（类型注解、docstring）
        - ✅ **不要修改与任务无关的文件**
        - ✅ **提交前运行所有测试**：`pytest`
        - ✅ **代码必须通过 flake8 和 mypy 检查**
        
        ### 📁 目录结构规则
        
        ```
        新模型 → backend/app/models/
        新服务 → backend/app/services/
        新 API → backend/app/api/v1/
        新钩子 → backend/app/hooks/
        新工具 → backend/app/utils/
        新测试 → backend/tests/unit/ 或 backend/tests/integration/
        ```
        
        ---
        
        **注意**: 
        - AI Agent 会自动阅读上述文档
        - 请提供清晰的验收标准
        - AI 生成的代码需要人工 Review
  
  - type: textarea
    id: task
    attributes:
      label: 任务描述
      description: 详细描述需要 AI 完成的任务
      placeholder: 请实现一个...功能，它能够...
    validations:
      required: true
  
  - type: textarea
    id: requirements
    attributes:
      label: 具体要求
      description: 列出所有必须满足的要求
      placeholder: |
        - 必须实现...
        - 需要支持...
        - 性能要求...
        - 安全要求...
    validations:
      required: true
  
  - type: textarea
    id: acceptance
    attributes:
      label: 验收标准
      description: 如何判断任务完成
      placeholder: |
        - [ ] 功能可以正常使用
        - [ ] 单元测试覆盖率 > 80%
        - [ ] 通过所有现有测试
        - [ ] 代码符合项目规范
    validations:
      required: true
  
  - type: dropdown
    id: complexity
    attributes:
      label: 复杂度
      description: 任务的复杂程度
      options:
        - 简单 (单一功能，< 50 行代码)
        - 中等 (多个功能，50-200 行代码)
        - 复杂 (系统功能，> 200 行代码)
    validations:
      required: true
  
  - type: textarea
    id: hints
    attributes:
      label: 实现提示 (可选)
      description: 给 AI 的实现建议
      placeholder: |
        建议参考...模块的实现
        可以使用...库
        注意...边界情况
  
  - type: textarea
    id: constraints
    attributes:
      label: 约束条件
      description: 实现时的限制
      placeholder: |
        - 不能修改...
        - 必须使用...
        - 需要兼容...
