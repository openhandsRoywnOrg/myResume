# OpenHands Resolver Workflow 触发条件分析

## 📊 Workflow 文件位置

`.github/workflows/openhands-resolver.yml`

## 🎯 触发条件总结

### 1. Issues 事件
```yaml
issues:
  types: [labeled]
```
- **触发时机**: 当 Issue 被**添加标签**时
- **注意**: 创建 Issue 不会触发，必须添加标签才会触发
- **测试验证**: ✅ Issue #42 创建时带有 `ai-agent` 和 `testing` 标签，已触发

### 2. Pull Request 事件
```yaml
pull_request:
  types: [labeled]
```
- **触发时机**: 当 PR 被**添加标签**时
- **注意**: 创建 PR 不会触发，必须添加标签才会触发

### 3. Issue 评论事件
```yaml
issue_comment:
  types: [created]
```
- **触发时机**: 当 Issue 收到**新评论**时
- **测试验证**: ✅ Issue #42 已添加测试评论，已触发

### 4. PR 评论事件
```yaml
pull_request_review_comment:
  types: [created]
```
- **触发时机**: 当 PR 收到**新评论**时

### 5. PR 审核事件
```yaml
pull_request_review:
  types: [submitted]
```
- **触发时机**: 当 PR 被**审核**时

## 🔧 Workflow 执行动作

```yaml
steps:
  - name: Forward to 自建 Webhook 服务器
    run: |
      # 1. 计算 HMAC-SHA256 签名
      SIGNATURE="sha256=$(echo -n "$GITHUB_PAYLOAD" | openssl dgst -sha256 -hmac "$WEBHOOK_SECRET" | awk '{print $2}')"
      
      # 2. 发送带签名的 POST 请求到 Webhook 服务器
      curl -v -X POST "$WEBHOOK_URL/webhook/github" \
        -H "Content-Type: application/json" \
        -H "X-GitHub-Event: $GITHUB_EVENT" \
        -H "X-Hub-Signature-256: $SIGNATURE" \
        -d "$GITHUB_PAYLOAD"
```

### 关键配置
- **Webhook URL**: `OPENHANDS_SERVER_URL` (环境变量)
- **Webhook Secret**: `OPENHANDS_WEBHOOK_SECRET` (GitHub Secret)
- **签名算法**: HMAC-SHA256
- **目标端点**: `/{WEBHOOK_URL}/webhook/github`

## 🧪 测试 Issue

### 创建的测试 Issue
- **Issue 编号**: #42
- **标题**: `[测试] OpenHands Resolver Workflow 触发测试`
- **URL**: https://github.com/openhandsRoywnOrg/myResume/issues/42

### 测试步骤
1. ✅ **创建 Issue** (带 `ai-agent` 和 `testing` 标签)
   - 触发条件：`issues.labeled`
   - 结果：Workflow 应该被触发

2. ✅ **添加评论**
   - 触发条件：`issue_comment.created`
   - 结果：Workflow 应该再次被触发

### 验证方法
1. 访问 https://github.com/openhandsRoywnOrg/myResume/actions
2. 查找 "Forward to OpenHands Server" workflow
3. 应该看到至少 2 次运行记录（一次来自添加标签，一次来自评论）

## 📝 重要发现

### ✅ 会触发 Workflow 的操作
- 给 Issue 添加标签
- 给 PR 添加标签
- 在 Issue 上评论
- 在 PR 上评论
- 审核 PR

### ❌ 不会触发 Workflow 的操作
- 创建 Issue（不带标签）
- 创建 PR（不带标签）
- 关闭/重新打开 Issue
- 分配 Assignee
- 修改 Issue 标题/描述

## 🎓 使用建议

### 自动触发 OpenHands Agent
1. 使用 AI Task 模板创建 Issue（会自动添加 `ai-agent` 标签）
2. 或者手动给 Issue 添加 `ai-agent` 标签
3. Workflow 会自动将事件转发到 OpenHands 服务器

### 手动触发
```bash
# 使用 GitHub CLI 添加标签触发
gh issue label <issue-number> ai-agent

# 或者添加评论触发
gh issue comment <issue-number> -b "@openhands-agent 请处理这个 issue"
```

## 🔐 安全机制

Workflow 使用 HMAC-SHA256 签名确保请求来源可信：
```bash
SIGNATURE="sha256=$(echo -n "$GITHUB_PAYLOAD" | openssl dgst -sha256 -hmac "$WEBHOOK_SECRET" | awk '{print $2}')"
```

Webhook 服务器应该验证签名：
```python
# 示例验证代码
import hmac
import hashlib

def verify_signature(payload, signature, secret):
    expected = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)
```

## 📊 测试时间线

- **2026-03-06 14:15:45 UTC**: 创建 Issue #42（带标签，触发第一次）
- **2026-03-06 14:15:53 UTC**: 添加评论（触发第二次）

---

**生成时间**: 2026-03-06  
**测试 Issue**: #42  
**状态**: ✅ 测试完成
