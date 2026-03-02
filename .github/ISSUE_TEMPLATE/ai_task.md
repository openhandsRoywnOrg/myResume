---
name: AI Agent 任务
description: 使用 @openhands-agent 自动解决任务
title: "[AI Task]: "
labels: ["ai-agent"]
body:
  - type: markdown
    attributes:
      value: |
        使用 AI Agent 自动解决开发任务。
        
        **注意**: 
        - AI Agent 会阅读 AGENTS.md 了解项目规范
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
