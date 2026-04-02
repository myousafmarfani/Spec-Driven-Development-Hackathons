# Dashboard

> **Last Updated:** {{TIMESTAMP}}  
> **System Status:** {{STATUS}}

---

## Quick Stats

| Metric | Today | This Week | This Month |
|--------|-------|-----------|------------|
| Emails Processed | {{EMAIL_COUNT}} | {{WEEK_EMAIL_COUNT}} | {{MONTH_EMAIL_COUNT}} |
| WhatsApp Messages | {{WA_COUNT}} | {{WEEK_WA_COUNT}} | {{MONTH_WA_COUNT}} |
| Invoices Sent | {{INVOICE_COUNT}} | {{WEEK_INVOICE_COUNT}} | {{MONTH_INVOICE_COUNT}} |
| Revenue | ${{REVENUE}} | ${{WEEK_REVENUE}} | ${{MONTH_REVENUE}} |
| Pending Approvals | {{PENDING_COUNT}} | - | - |

---

## Inbox (Needs Action)

<!-- Auto-populated by Orchestrator -->
{{NEEDS_ACTION_LIST}}

---

## Pending Approval

**Action Required:** Move these files to `/Approved/` or `/Rejected/`

<!-- Auto-populated by Orchestrator -->
{{PENDING_APPROVAL_LIST}}

---

## Recent Activity

<!-- Auto-populated by Orchestrator -->
{{RECENT_ACTIVITY}}

---

## System Health

| Component | Status | Last Check |
|-----------|--------|------------|
| Gmail Watcher | {{GMAIL_STATUS}} | {{GMAIL_LAST_CHECK}} |
| WhatsApp Watcher | {{WA_STATUS}} | {{WA_LAST_CHECK}} |
| File Watcher | {{FILE_STATUS}} | {{FILE_LAST_CHECK}} |
| Orchestrator | {{ORCHESTRATOR_STATUS}} | {{ORCHESTRATOR_LAST_CHECK}} |
| Watchdog | {{WATCHDOG_STATUS}} | {{WATCHDOG_LAST_CHECK}} |

---

## Alerts

<!-- Auto-populated by Watchdog -->
{{ALERTS}}

---

## Today's Schedule

| Time | Event | Status |
|------|-------|--------|
| 08:00 | CEO Briefing | {{BRIEFING_STATUS}} |
| {{TIME}} | {{EVENT}} | {{STATUS}} |

---

## Revenue Tracker

### This Month

| Date | Description | Amount | Status |
|------|-------------|--------|--------|
| {{DATE}} | {{DESC}} | ${{AMOUNT}} | {{STATUS}} |

**Total:** ${{MONTH_TOTAL}}

---

## Top Contacts (This Week)

| Contact | Messages | Last Contact |
|---------|----------|--------------|
| {{CONTACT}} | {{COUNT}} | {{DATE}} |

---

## Quick Actions

- [ ] Review pending approvals
- [ ] Check system health
- [ ] Review logs
- [ ] Update business goals

---

## Notes

{{NOTES}}

---

*Dashboard auto-updates every 5 minutes. Last full refresh: {{LAST_REFRESH}}*
