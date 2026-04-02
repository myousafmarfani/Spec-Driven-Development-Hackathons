# Troubleshooting Guide

Common issues and solutions for the AI Employee Bronze Tier.

---

## Setup Issues

### Q: Claude Code says "command not found"

**A:** Ensure Claude Code is installed globally:

```bash
npm install -g @anthropic/claude-code

# Verify installation
claude --version
```

Restart your terminal after installation.

---

### Q: Obsidian vault isn't being read by Claude

**A:** Check the following:

1. Run Claude Code from the vault directory:
   ```bash
   cd hackathon-0-bronze-tier
   claude --prompt "..."
   ```

2. Or use the `--cwd` flag:
   ```bash
   claude --cwd ./Vault --prompt "..."
   ```

3. Verify file permissions allow read access.

---

### Q: Gmail API returns 403 Forbidden

**A:** Check Google Cloud Console settings:

1. Enable Gmail API for your project
2. Configure OAuth consent screen
3. Add your redirect URI: `http://localhost:8080`
4. Download credentials to `credentials/credentials.json`

See: https://developers.google.com/gmail/api/quickstart

---

### Q: Playwright MCP server won't start

**A:** Try these steps:

```bash
# 1. Kill any existing processes
pkill -f "@playwright/mcp"

# 2. Clear temp files
rm -rf /tmp/playwright-mcp-*

# 3. Start fresh
bash .qwen/skills/browsing-with-playwright/scripts/start-server.sh

# 4. Verify
python .qwen/skills/browsing-with-playwright/scripts/verify.py
```

---

## Runtime Issues

### Q: Watcher scripts stop running overnight

**A:** Use PM2 process manager:

```bash
# Install PM2
npm install -g pm2

# Start all processes
pm2 start ecosystem.config.js

# Save process list (starts on reboot)
pm2 save

# Setup startup
pm2 startup
```

---

### Q: Claude is making incorrect decisions

**A:** Review and update your `Company_Handbook.md`:

1. Add more specific rules
2. Lower autonomy thresholds
3. Require approval for more actions
4. Review past decisions in `Vault/Done/`

Example adjustment:
```markdown
## Payment Rules
- ALWAYS require approval for payments > $50
- NEVER auto-approve new payees
```

---

### Q: MCP server won't connect

**A:** Check the following:

```bash
# 1. Verify server is running
pgrep -f "@playwright/mcp"

# 2. Check port
netstat -an | grep 8808

# 3. Test connection
python .qwen/skills/browsing-with-playwright/scripts/verify.py

# 4. Restart if needed
bash .qwen/skills/browsing-with-playwright/scripts/stop-server.sh
bash .qwen/skills/browsing-with-playwright/scripts/start-server.sh
```

---

### Q: Files not moving between folders

**A:** Check file permissions:

```bash
# On Linux/Mac
chmod -R 755 Vault/

# On Windows (PowerShell)
icacls Vault /grant Users:F /T
```

---

## Security Concerns

### Q: How do I know my credentials are safe?

**A:** Follow these practices:

1. **Never commit `.env`** - Added to `.gitignore`
2. **Use environment variables** - Not hardcoded
3. **Rotate credentials regularly** - Especially after testing
4. **Review audit logs** - `Vault/Logs/` daily

Check for exposed credentials:
```bash
# Search for potential leaks
git log -p | grep -i "password\|secret\|token"
```

---

### Q: What if Claude tries to pay the wrong person?

**A:** This is why HITL is critical:

1. **Payment thresholds** - Set low auto-approve limits
2. **Approval workflow** - All payments require approval
3. **Audit trail** - Every action logged
4. **Quick stop** - `pm2 stop all` in emergencies

---

## Performance Issues

### Q: System is slow to respond

**A:** Adjust polling intervals in `.env`:

```bash
# Faster response (more CPU)
GMAIL_POLL_INTERVAL=30
WHATSAPP_POLL_INTERVAL=15
ORCHESTRATOR_CHECK_INTERVAL=10

# Slower response (less CPU)
GMAIL_POLL_INTERVAL=120
WHATSAPP_POLL_INTERVAL=60
ORCHESTRATOR_CHECK_INTERVAL=60
```

---

### Q: High memory usage

**A:** Check for memory leaks:

```bash
# Monitor memory
pm2 monit

# Restart high-memory processes
pm2 restart orchestrator

# Set memory limits in ecosystem.config.js
```

---

## Log Analysis

### View Recent Errors

```bash
# Last 50 lines of today's log
tail -50 Vault/Logs/$(date +%Y-%m-%d).log

# Search for errors
grep "ERROR" Vault/Logs/*.log | tail -20

# JSON logs
cat Vault/Logs/*.jsonl | jq 'select(.level == "ERROR")'
```

---

### Export Logs

```bash
# Combine all logs
cat Vault/Logs/*.jsonl > all_logs.jsonl

# Filter by date
jq 'select(.timestamp | startswith("2026-01-07"))' all_logs.jsonl

# Filter by action type
jq 'select(.action_type == "email_send")' all_logs.jsonl
```

---

## Reset Everything

### Full Reset

```bash
# 1. Stop all processes
pm2 stop all
pkill -f "@playwright/mcp"

# 2. Clear temp files
rm -rf /tmp/ai_employee/
rm -rf /tmp/playwright-mcp-*

# 3. Clear processed files
rm Vault/Needs_Action/*.md
rm Vault/Plans/*.md
rm Vault/Pending_Approval/*.md
rm Vault/Approved/*.md
rm Vault/Rejected/*.md

# 4. Restart
pm2 start ecosystem.config.js
bash .qwen/skills/browsing-with-playwright/scripts/start-server.sh
```

---

## Get Help

1. **Check documentation**: `README.md`, `DEMO.md`
2. **Review logs**: `Vault/Logs/`
3. **Test in dry-run**: `export DRY_RUN=true`
4. **Consult handbook**: `Vault/Company_Handbook.md`

---

**Still having issues?** Create a detailed bug report with:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Relevant log excerpts
