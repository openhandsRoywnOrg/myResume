# OpenHands Agent 配置说明

## 📄 文件说明

`.openhands/config.yaml` 是 OpenHands AI Agent 的配置文件，定义了：

- AI Agent 的行为规范
- 项目代码规范
- 目录结构规则
- 自动化检查
- GitHub 集成配置

## 🎯 核心功能

### 1. 必读文档配置

AI Agent 在开始工作前会自动读取以下文档：

```yaml
agent:
  required_docs:
    - "AGENTS.md"                    # ⭐ 最重要
    - "ARCHITECTURE_PLAN.md"
    - "backend/README.md"
    - "docs/ISSUE_GUIDELINES.md"
    - "backend/docs/CONFIG_GUIDE.md"
```

**作用**：确保 AI 了解项目规范和架构

### 2. 代码风格要求

```yaml
agent:
  code_style:
    type_annotations: "required"     # 必须有类型注解
    docstrings: "required"           # 必须有文档字符串
    test_coverage_target: 80         # 测试覆盖率目标 80%
```

**作用**：保证代码质量一致性

### 3. 目录结构规则

```yaml
agent:
  directory_rules:
    models: "backend/app/models/"
    services: "backend/app/services/"
    api: "backend/app/api/v1/"
    hooks: "backend/app/hooks/"
    utils: "backend/app/utils/"
    unit_tests: "backend/tests/unit/"
```

**作用**：确保代码组织有序

### 4. 自动检查

```yaml
agent:
  auto_checks:
    run_tests: true
    check_style: true
    check_types: true
    verify_imports: true
    check_coverage: true
    min_coverage: 80
```

**作用**：提交前自动验证代码质量

### 5. 禁止操作

```yaml
agent:
  forbidden_actions:
    - "modify_main_branch_directly"
    - "delete_existing_tests"
    - "modify_unrelated_files"
    - "commit_sensitive_data"
    - "skip_tests"
```

**作用**：防止 AI 执行危险操作

### 6. GitHub 集成

```yaml
github:
  auto_pr: true
  required_checks:
    - "tests_pass"
    - "style_check"
    - "type_check"
  auto_labels:
    - "ai-generated"
    - "needs-review"
```

**作用**：自动化 PR 流程

## 🔧 使用方法

### AI Agent 自动读取

当 OpenHands Agent 处理 Issue 时，会自动：

1. 读取 `.openhands/config.yaml`
2. 加载 `required_docs` 中的文档
3. 应用 `code_style` 规则
4. 遵循 `directory_rules`
5. 执行 `auto_checks`
6. 创建符合 `github` 配置的 PR

### 手动覆盖配置

在 Issue 中可以临时覆盖某些配置：

```markdown
## 特殊要求

- 本次任务不需要类型检查：`check_types: false`
- 测试覆盖率可以低于 80%：`min_coverage: 60`
```

## 📋 配置项详解

### agent.required_docs

**类型**: 列表
**默认**: 见配置文件
**说明**: AI 必读文档列表，路径相对于项目根目录

### agent.code_style

**类型**: 字典
**选项**:
- `type_annotations`: "required" | "optional" | "none"
- `docstrings`: "required" | "optional" | "none"
- `test_coverage_target`: 0-100 的整数

### agent.directory_rules

**类型**: 字典
**说明**: 定义各类代码的存放位置
**键**: 代码类型（models, services, api 等）
**值**: 目录路径

### agent.auto_checks

**类型**: 字典
**选项**:
- `run_tests`: true | false
- `check_style`: true | false
- `check_types`: true | false
- `check_coverage`: true | false
- `min_coverage`: 0-100 的整数

### agent.forbidden_actions

**类型**: 列表
**说明**: AI 不允许执行的操作
**选项**:
- `modify_main_branch_directly`: 直接修改 main 分支
- `delete_existing_tests`: 删除现有测试
- `modify_unrelated_files`: 修改无关文件
- `commit_sensitive_data`: 提交敏感数据
- `skip_tests`: 跳过测试

### github.auto_pr

**类型**: 布尔值
**默认**: true
**说明**: 是否自动创建 Pull Request

### github.required_checks

**类型**: 列表
**说明**: PR 合并前必须通过的检查
**选项**:
- `tests_pass`: 测试通过
- `style_check`: 代码风格检查
- `type_check`: 类型检查

## 🚨 注意事项

### 1. 不要提交敏感信息

配置文件中不要包含：
- API 密钥
- 数据库密码
- 私人令牌

这些应该通过环境变量设置。

### 2. 谨慎修改 directory_rules

修改目录规则可能导致 AI 把代码放到错误的位置。

### 3. 测试覆盖率目标

设置合理的覆盖率目标：
- 太低（< 60%）：代码质量无法保证
- 太高（> 90%）：可能浪费时间在边缘情况

推荐：80%

### 4. 自动检查性能

启用太多自动检查可能减慢 AI 工作速度。
建议只启用必要的检查。

## 🔍 调试

### 查看 AI 读取的配置

在 Issue 评论中添加：

```
@openhands-agent 请显示你读取的配置
```

AI 会输出它读取的配置信息。

### 验证配置语法

```bash
# 使用 yamllint 验证 YAML 语法
yamllint .openhands/config.yaml
```

### 测试配置

创建一个测试 Issue：

```markdown
[AI Task]: 测试配置是否生效

任务：创建一个简单的函数，验证 AI 是否遵循配置

要求：
- 函数必须有类型注解
- 函数必须有 docstring
- 必须有单元测试
```

观察 AI 生成的代码是否符合配置。

## 📚 参考资源

- [OpenHands 文档](https://docs.openhands.dev/)
- [YAML 配置指南](https://yaml.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

**最后更新**: 2026-03-01
**版本**: 0.1.0
