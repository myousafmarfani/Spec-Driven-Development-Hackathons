# Demo Guide: End-to-End Invoice Flow

> This guide walks through the complete flow from WhatsApp message to invoice sent, demonstrating all Bronze Tier components working together.

---

## Scenario

A client sends a WhatsApp message asking for an invoice. The AI Employee should:
1. Detect the request
2. Generate the invoice
3. Request human approval
4. Send via email
5. Log the transaction

---

## Step 1: Detection (WhatsApp Watcher)

### Start WhatsApp Watcher

```bash
# Start Playwright MCP server first
bash .qwen/skills/browsing-with-playwright/scripts/start-server.sh

# Start WhatsApp watcher
python src/watchers/whatsapp_watcher.py
```

### Client Sends Message

**WhatsApp Message:**
```
Hey, can you send me the invoice for January?
- From: Client A (client_a@email.com)
```

### Watcher Detects Trigger

The WhatsApp Watcher:
1. Polls WhatsApp Web every 30 seconds
2. Extracts message content
3. Detects trigger keyword: "invoice"
4. Creates action file

### Action File Created

**File:** `Vault/Needs_Action/WHATSAPP_client_a_20260107_103000.md`

```markdown
---
created: 2026-01-07T10:30:00Z
source: whatsapp
sender: Client A
text: Hey, can you send me the invoice for January?
triggers: keyword:invoice
status: pending
---

# WhatsApp Message Received

**From:** Client A  
**Time:** 2026-01-07T10:30:00Z

## Message Content

Hey, can you send me the invoice for January?

## Detected Triggers

keyword:invoice

## Suggested Actions

<!-- Qwen Code will populate this -->

## Processing Log

- [2026-01-07T10:30:00Z] Detected by WhatsApp Watcher
- [2026-01-07T10:30:00Z] Triggers: keyword:invoice
```

---

## Step 2: Reasoning (Orchestrator + Qwen Code)

### Orchestrator Detects New File

```bash
# Orchestrator polls every 30 seconds
python src/orchestrator.py
```

**Orchestrator Log:**
```
2026-01-07 10:30:30 [INFO] Processing: WHATSAPP_client_a_20260107_103000.md
2026-01-07 10:30:30 [INFO] Invoking Qwen Code for: WHATSAPP_client_a_20260107_103000.md
```

### Qwen Code Analyzes

Qwen Code reads the action file and creates a plan:

**File:** `Vault/Plans/PLAN_WHATSAPP_client_a_20260107_103000.md`

```markdown
---
created: 2026-01-07T10:30:35Z
status: pending_approval
source: whatsapp
input_file: Vault/Needs_Action/WHATSAPP_client_a_20260107_103000.md
---

# Action Plan

## Objective
Generate and send January invoice to Client A

## Steps
- [x] Identify client: Client A (client_a@email.com)
- [x] Calculate amount: $1,500 (from Vault/Accounting/Rates.md)
- [ ] Generate invoice PDF
- [ ] Send via email (REQUIRES APPROVAL)
- [ ] Log transaction

## Approval Required
Email send requires human approval. See Vault/Pending_Approval/

## Client Details
- Name: Client A
- Email: client_a@email.com
- Service: Consulting (January 2026)
- Amount: $1,500 (10 hours @ $150/hour)
```

---

## Step 3: Approval Request (Human-in-the-Loop)

### Approval File Created

**File:** `Vault/Pending_Approval/APPROVAL_PLAN_WHATSAPP_client_a_20260107_103000.md`

```markdown
---
created: 2026-01-07T10:30:40Z
plan_file: Vault/Plans/PLAN_WHATSAPP_client_a_20260107_103000.md
objective: Generate and send January invoice to Client A
status: pending
---

# Approval Required

**Objective:** Generate and send January invoice to Client A

**Plan:** PLAN_WHATSAPP_client_a_20260107_103000.md

## Instructions

1. Review the plan file above
2. If you approve, move this file to `/Approved/`
3. If you reject, move this file to `/Rejected/`

## Invoice Details

- **To:** Client A (client_a@email.com)
- **Amount:** $1,500
- **Period:** January 2026
- **Service:** Consulting (10 hours)

## Email Preview

**Subject:** January 2026 Invoice - $1,500  
**Body:**
```
Dear Client A,

Please find attached your invoice for January 2026.

Invoice Details:
- Service: Consulting
- Hours: 10
- Rate: $150/hour
- Total: $1,500

Payment is due within 30 days.

Best regards,
[Your Company]

---
Sent with AI assistance
```
```

### Human Reviews

**You (the human):**
1. Open Obsidian
2. Navigate to `Vault/Pending_Approval/`
3. Review the approval request
4. Verify client and amount
5. Move file to `Vault/Approved/`

---

## Step 4: Execution (Orchestrator + MCP)

### Orchestrator Detects Approval

```bash
# Orchestrator polls Approved folder
2026-01-07 10:35:00 [INFO] Executing approved action: APPROVAL_PLAN_WHATSAPP_client_a_20260107_103000.md
2026-01-07 10:35:00 [INFO] Executing email send action: client_a@email.com - January 2026 Invoice
```

### Generate Invoice PDF

**File:** `Vault/Invoices/2026-01_Client_A.pdf`

```markdown
# INVOICE

**Invoice Number:** INV-2026-001  
**Date:** January 7, 2026  
**Due Date:** February 6, 2026

---

**From:**
[Your Company]
[Your Address]

**To:**
Client A
[Client Address]

---

| Description | Quantity | Rate | Amount |
|-------------|----------|------|--------|
| Consulting Services (January 2026) | 10 hours | $150 | $1,500 |

---

**Total Due:** $1,500

**Payment Instructions:**
[Bank details or payment link]
```

### Email Sent via MCP

The Orchestrator calls Email MCP:

```python
# src/mcp/email_mcp.py
email_mcp.send_email(
    to='client_a@email.com',
    subject='January 2026 Invoice - $1,500',
    body='Please find attached your invoice...',
    attachments=['Vault/Invoices/2026-01_Client_A.pdf']
)
```

**Browser Automation (via Playwright MCP):**
1. Navigate to Gmail compose
2. Fill recipient: client_a@email.com
3. Fill subject: January 2026 Invoice - $1,500
4. Fill body
5. Attach PDF
6. Click Send

---

## Step 5: Completion

### File Moved to Done

```bash
# Orchestrator moves files to Done
mv Vault/Approved/APPROVAL_*.md Vault/Done/
mv Vault/Plans/PLAN_*.md Vault/Done/
```

### Dashboard Updated

**File:** `Vault/Dashboard.md`

```markdown
# Dashboard

> **Last Updated:** 2026-01-07T10:35:30Z  
> **System Status:** Running

## Quick Stats

| Metric | Today | This Week | This Month |
|--------|-------|-----------|------------|
| Emails Processed | 1 | 1 | 1 |
| Invoices Sent | 1 | 1 | 1 |
| Revenue | $1,500 | $1,500 | $1,500 |
| Pending Approvals | 0 | - | - |

## Recent Activity

- [2026-01-07 10:35] Invoice sent to Client A ($1,500)
```

### Transaction Logged

**File:** `Vault/Logs/2026-01-07.jsonl`

```json
{
  "timestamp": "2026-01-07T10:35:30Z",
  "action_type": "email_send",
  "actor": "ai_employee",
  "target": "client_a@email.com",
  "parameters": {
    "subject": "January 2026 Invoice - $1,500",
    "attachment": "Vault/Invoices/2026-01_Client_A.pdf"
  },
  "approval_status": "approved",
  "approved_by": "human",
  "result": "success"
}
```

---

## Full Timeline

| Time | Event |
|------|-------|
| 10:30:00 | Client sends WhatsApp message |
| 10:30:05 | WhatsApp Watcher detects trigger |
| 10:30:10 | Action file created in Needs_Action |
| 10:30:30 | Orchestrator picks up action |
| 10:30:35 | Qwen Code creates plan |
| 10:30:40 | Approval request created |
| 10:35:00 | Human approves (moves to Approved) |
| 10:35:05 | Orchestrator detects approval |
| 10:35:10 | Invoice PDF generated |
| 10:35:20 | Email sent via MCP |
| 10:35:30 | Files moved to Done |
| 10:35:35 | Dashboard updated |
| 10:35:40 | Transaction logged |

**Total Time:** ~6 minutes (mostly waiting for human approval)

---

## Testing the Flow

### Manual Test

```bash
# 1. Create test action file
cat > Vault/Needs_Action/TEST_invoice_$(date +%Y%m%d_%H%M%S).md << 'EOF'
---
created: $(date -Iseconds)
source: test
triggers: keyword:invoice
status: pending
---

# Test Invoice Request

**From:** Test Client  
**Request:** Send invoice for $100

## Suggested Actions
- Generate invoice
- Send via email
EOF

# 2. Run orchestrator once
python src/orchestrator.py --once

# 3. Check Pending_Approval folder
ls Vault/Pending_Approval/

# 4. Review and approve (move to Approved)
mv Vault/Pending_Approval/*.md Vault/Approved/

# 5. Run orchestrator to execute
python src/orchestrator.py --once

# 6. Check Done folder
ls Vault/Done/
```

### Verify Results

```bash
# Check logs
cat Vault/Logs/$(date +%Y-%m-%d).log

# Check dashboard
cat Vault/Dashboard.md

# Check transaction log
cat Vault/Logs/$(date +%Y-%m-%d).jsonl
```

---

## Troubleshooting

### Issue: WhatsApp Watcher Not Detecting

**Solution:**
1. Check Playwright MCP server: `bash scripts/start-server.sh`
2. Verify WhatsApp Web is logged in
3. Check watcher logs: `cat Vault/Logs/*.log | grep whatsapp`

### Issue: Qwen Code Not Available

**Solution:**
1. Install Qwen Code
2. Verify: `qwen --version`
3. Test: `qwen --prompt "hello"`

### Issue: Email Not Sending

**Solution:**
1. Check MCP server: `python scripts/verify.py`
2. Verify Gmail authentication
3. Run in dry-run mode first: `export DRY_RUN=true`

---

## Next Steps

After mastering the invoice flow:

1. **Add Gmail Watcher**: Auto-process email invoice requests
2. **Add Payment Processing**: Connect banking API
3. **Add Social Media**: Auto-post invoices as content
4. **Add Reporting**: Weekly revenue reports

---

**Congratulations!** You've completed the End-to-End Invoice Flow demo.
