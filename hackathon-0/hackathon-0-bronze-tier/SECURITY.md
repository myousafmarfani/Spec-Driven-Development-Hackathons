# Security Guide

> **Important:** This document outlines security best practices for the AI Employee system. Read and understand before deploying.

---

## Credential Management

### Never Commit Secrets

```bash
# Add to .gitignore
.env
credentials/
*.pem
*.key
```

### Environment Variables

Store all sensitive credentials in `.env` file:

```bash
# Copy template
cp .env.example .env

# Edit with your credentials
nano .env  # or use your preferred editor
```

### Credential Storage

| Credential | Storage Method |
|------------|---------------|
| API Keys | Environment variables |
| OAuth Tokens | Encrypted file in `credentials/` |
| Passwords | Password manager (not in code) |
| SSH Keys | System keychain |

---

## Human-in-the-Loop (HITL) Safeguards

### Required Approval

The following actions **always** require human approval:

1. **Payments**
   - Any payment to new payee
   - Any payment > $100
   - International transfers

2. **Communications**
   - Emails to new contacts
   - Bulk emails (> 5 recipients)
   - Social media replies/DMs

3. **File Operations**
   - Deleting files
   - Moving files outside Vault
   - Modifying system configuration

### Approval Workflow

```
┌─────────────┐    ┌──────────────┐    ┌──────────┐
│ AI Request  │ →  │ Human Review │ →  │ Approved │
└─────────────┘    └──────────────┘    └──────────┘
                          ↓
                    ┌──────────┐
                    │ Rejected │
                    └──────────┘
```

---

## Sandboxing

### Development Mode

Run in development mode to prevent real actions:

```bash
export DEV_MODE=true
export DRY_RUN=true

python src/orchestrator.py
```

### Dry Run Flag

All action scripts support `--dry-run`:

```bash
# Test without executing
python src/orchestrator.py --dry-run

# Test watchers
python src/watchers/gmail_watcher.py --dry-run
```

### Separate Accounts

Use test/sandbox accounts during development:

- **Gmail**: Create test Gmail account
- **Banking**: Use sandbox API if available
- **Social Media**: Use test accounts

---

## Rate Limiting

### Default Limits

| Action | Limit |
|--------|-------|
| Emails/hour | 10 |
| Payments/hour | 3 |
| Social posts/hour | 5 |
| API calls/minute | 60 |

### Configure Limits

Edit `src/hitl.py` to adjust thresholds:

```python
APPROVAL_THRESHOLDS = {
    'email': {
        'max_per_hour': 10,
        # ...
    }
}
```

---

## Audit Logging

### Log Location

All logs stored in: `Vault/Logs/`

### Log Format

```json
{
  "timestamp": "2026-01-07T10:30:00Z",
  "action_type": "email_send",
  "actor": "ai_employee",
  "target": "client@example.com",
  "parameters": {"subject": "Invoice #123"},
  "approval_status": "approved",
  "approved_by": "human",
  "result": "success"
}
```

### Log Retention

- **Active logs**: 7 days (rotated daily)
- **Archive**: 90 days minimum
- **Compliance**: Retain as required by your jurisdiction

### Review Logs

```bash
# View today's logs
cat Vault/Logs/$(date +%Y-%m-%d).log

# Search logs
grep "payment" Vault/Logs/*.jsonl
```

---

## Access Control

### File Permissions

```bash
# Restrict vault access
chmod 700 Vault/

# Restrict credentials
chmod 600 credentials/
```

### Process Isolation

Run watchers in separate processes:

```bash
# Use PM2 for process management
pm2 start ecosystem.config.js
```

### Network Security

- Use HTTPS for all API calls
- Never send credentials in URLs
- Validate SSL certificates

---

## Error Handling

### Graceful Degradation

When components fail:

1. **Gmail API down**: Queue emails locally
2. **Banking API timeout**: Never retry payments automatically
3. **Claude Code unavailable**: Queue for later processing
4. **Obsidian vault locked**: Write to temp folder

### Retry Logic

```python
# Automatic retry with backoff
@with_retry(max_attempts=3, base_delay=1)
def send_email():
    # ...
```

### Circuit Breaker

Prevent cascade failures:

```python
# Stop trying after repeated failures
if failures > 5:
    alert_human()
    pause_operations()
```

---

## Monitoring

### Health Checks

```bash
# Check all processes
python src/watchdog.py --status

# View alerts
cat Vault/Logs/alerts.json
```

### Daily Review

Recommended daily checklist:

1. [ ] Review `Vault/Dashboard.md`
2. [ ] Check pending approvals
3. [ ] Review error logs
4. [ ] Verify watcher status

### Weekly Audit

1. Review all payment actions
2. Check approval rejection rate
3. Analyze error patterns
4. Update thresholds if needed

---

## Incident Response

### If AI Misbehaves

1. **Stop immediately**:
   ```bash
   pm2 stop all
   # or
   python src/watchdog.py --stop
   ```

2. **Review logs**:
   ```bash
   tail -f Vault/Logs/*.log
   ```

3. **Identify cause**:
   - Check recent approvals
   - Review threshold settings
   - Analyze error messages

4. **Fix and restart**:
   - Update configuration
   - Test in dry-run mode
   - Restart with monitoring

### Recovery Procedure

1. Stop all processes
2. Backup current state
3. Fix configuration/code
4. Test in isolation
5. Restart one process at a time
6. Monitor closely

---

## Best Practices

### DO

- ✅ Review all approvals before confirming
- ✅ Start with `DRY_RUN=true`
- ✅ Monitor logs daily
- ✅ Rotate credentials regularly
- ✅ Use separate test accounts
- ✅ Set up alerts for failures

### DON'T

- ❌ Commit `.env` to version control
- ❌ Run without HITL initially
- ❌ Auto-approve payments > $100
- ❌ Share credentials via email
- ❌ Skip log reviews
- ❌ Deploy without testing

---

## Compliance Considerations

### Data Privacy

- **GDPR**: Ensure consent for data processing
- **CCPA**: Allow opt-out of data collection
- **Local laws**: Consult legal counsel

### Financial Regulations

- **Record keeping**: Retain transaction logs
- **Audit trail**: Maintain approval history
- **Reporting**: Generate compliance reports

### Terms of Service

Review ToS for all integrated services:
- Gmail API
- WhatsApp (business use)
- Banking APIs
- Social media platforms

---

## Security Checklist

Before going live:

- [ ] All credentials in `.env` (not hardcoded)
- [ ] `.env` added to `.gitignore`
- [ ] HITL enabled for all critical actions
- [ ] Rate limits configured
- [ ] Logging verified
- [ ] Alert system tested
- [ ] Backup procedure in place
- [ ] Recovery procedure documented
- [ ] Test run completed successfully

---

## Contact

For security concerns or questions:
- Review documentation in `Vault/Company_Handbook.md`
- Check logs in `Vault/Logs/`
- Consult security best practices online

---

**Remember:** You are responsible for all actions taken by your AI Employee. Regular oversight is essential.
