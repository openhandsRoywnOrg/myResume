---
name: Bug 报告
description: 报告项目中的错误或问题
title: "[Bug]: "
labels: ["bug"]
body:
  - type: markdown
    attributes:
      value: |
        感谢报告 Bug！请提供尽可能多的信息帮助我们定位问题。
  
  - type: textarea
    id: description
    attributes:
      label: Bug 描述
      description: 清晰简洁地描述这个 Bug
      placeholder: 当...时，发生了...，期望的行为是...
    validations:
      required: true
  
  - type: textarea
    id: reproduction
    attributes:
      label: 复现步骤
      description: 如何复现这个 Bug
      placeholder: |
        1. 进入 '...'
        2. 点击 '...'
        3. 滚动到 '...'
        4. 出现错误
    validations:
      required: true
  
  - type: textarea
    id: expected
    attributes:
      label: 期望的行为
      description: 正常情况下应该发生什么
      placeholder: 期望看到...
    validations:
      required: true
  
  - type: textarea
    id: actual
    attributes:
      label: 实际的行为
      description: 实际发生了什么
      placeholder: 实际看到了...错误信息/行为
    validations:
      required: true
  
  - type: textarea
    id: environment
    attributes:
      label: 环境信息
      description: 您的运行环境
      placeholder: |
        - OS: [e.g. Ubuntu 22.04]
        - Python: [e.g. 3.10]
        - Browser: [e.g. Chrome 120]
    validations:
      required: true
  
  - type: textarea
    id: logs
    attributes:
      label: 日志信息
      description: 相关的错误日志或截图
      placeholder: 粘贴错误日志或截图...
      render: shell
  
  - type: dropdown
    id: severity
    attributes:
      label: 严重程度
      description: 这个 Bug 的影响程度
      options:
        - 低 (界面小问题，不影响功能)
        - 中 (部分功能受影响，有替代方案)
        - 高 (核心功能受影响，无替代方案)
        - 严重 (系统崩溃，数据丢失)
    validations:
      required: true
  
  - type: checkboxes
    id: terms
    attributes:
      label: 确认
      description: 请确认以下事项
      options:
        - label: 我已经搜索了现有的 Issue，没有重复报告
          required: true
        - label: 我提供了足够的复现信息
          required: true
