# OpenHands 自建 Webhook 服务器

## 部署

```bash
bash scripts/deploy-webhook-server.sh
```

## 配置 GitHub Secrets

```bash
gh secret set OPENHANDS_SERVER_URL --body="http://your-server-ip:5001"
gh secret set OPENHANDS_WEBHOOK_SECRET --body="your-secret"
```

## 测试

```bash
gh issue create --title "Test" --label "ai-agent"
```
