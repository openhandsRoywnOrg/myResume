---
name: 功能请求
description: 为项目提出新功能或改进建议
title: "[Feature]: "
labels: ["enhancement"]
body:
  - type: markdown
    attributes:
      value: |
        感谢您提出功能建议！请尽可能详细地描述您的需求。
  
  - type: textarea
    id: problem
    attributes:
      label: 相关的问题
      description: 您的功能建议是否解决了某个问题？请描述。
      placeholder: 当我在使用...时，遇到了...问题
    validations:
      required: true
  
  - type: textarea
    id: solution
    attributes:
      label: 期望的解决方案
      description: 描述您希望实现的功能
      placeholder: 我希望可以...，这样就能...
    validations:
      required: true
  
  - type: textarea
    id: alternatives
    attributes:
      label: 其他考虑的方案
      description: 您考虑过哪些替代方案？
      placeholder: 我也考虑过...，但是...
  
  - type: dropdown
    id: priority
    attributes:
      label: 优先级
      description: 这个功能的重要程度
      options:
        - 低 (有空再做)
        - 中 (可以排期)
        - 高 (影响核心功能)
        - 紧急 (阻碍其他工作)
    validations:
      required: true
  
  - type: textarea
    id: acceptance
    attributes:
      label: 验收标准
      description: 如何判断这个功能已经完成？
      placeholder: |
        - [ ] 用户可以...
        - [ ] 系统能够...
        - [ ] 性能达到...
    validations:
      required: true
  
  - type: textarea
    id: context
    attributes:
      label: 补充信息
      description: 任何其他背景信息、截图或示例
      placeholder: 这里可以添加更多细节...
