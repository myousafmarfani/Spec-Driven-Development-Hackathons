# Personal AI Employee - Bronze Tier

## Project Overview

This is a **Digital FTE (Full-Time Equivalent)** — an AI agent system that works 24/7 to manage personal and business affairs. It uses **Qwen Code** as the reasoning engine and **Obsidian** as a local-first Markdown dashboard/vault. The system monitors external sources (Gmail, WhatsApp, filesystem, banking), creates action plans, requires human-in-the-loop approval for critical decisions, and executes approved actions via MCP (Model Context Protocol) servers.

### Architecture

```
External Sources → Watchers → Obsidian Vault → Qwen Code → MCP Servers → Actions
   (Gmail,           (Python    (Local         (Reasoning    (Email,       (Send Email,
    WhatsApp,        Scripts)    Markdown)      Engine)       Browser)       Post Social)
    Bank, Files)
                         ↓
                    Human-in-the-Loop Approval
```

### Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Brain** | Qwen Code | Reasoning engine |
| **Memory/GUI** | Obsidian | Local Markdown dashboard |
| **Senses** | Python Watchers | Monitor Gmail, WhatsApp, filesystem |
| **Hands** | MCP Servers | External actions (email, browser) |
| **Orchestration** | Python | Master process + watchdog |

## Project Structure

```
hackathon-0-bronze-tier/
├── Vault/                          # Obsidian vault (local-first knowledge base)
│   ├── Needs_Action/               # Incoming triggers from watchers
│   ├── Plans/                      # Qwen-generated action plans
│   ├── Pending_Approval/           # Awaiting human approval
│   ├── Approved/                   # Ready for execution
│   ├── Rejected/                   # Declined actions
│   ├── Done/                       # Completed tasks
│   ├── Logs/                       # Audit logs
│   ├── Invoices/                   # Generated invoices
│   ├── Agents/                     # Agent configurations
│   ├── Dashboard.md                # Main dashboard
│   ├── Company_Handbook.md         # Rules and guidelines
│   └── Business_Goals.md           # Objectives and metrics
├── src/                            # Python source code
│   ├── orchestrator.py             # Master process — polls vault folders, invokes Qwen Code, executes approved actions
│   ├── watchdog.py                 # Health monitor — restarts failed processes, alerts on failures
│   ├── hitl.py                     # Human-in-the-Loop approval system with auto-approve thresholds
│   ├── watchers/                   # Sentinel scripts
│   │   ├── gmail_watcher.py        # Monitors Gmail for triggers
│   │   ├── whatsapp_watcher.py     # Monitors WhatsApp Web via Playwright
│   │   └── file_watcher.py         # Watches filesystem for changes
│   ├── mcp/                        # MCP client integrations
│   │   └── email_mcp.py            # Email sending via MCP
│   └── utils/
│       └── logger.py               # Structured JSON + console logging with rotation
├── scripts/                        # Helper scripts (currently empty)
├── .env.example                    # Environment template
├── requirements.txt                # Python dependencies
├── ecosystem.config.js             # PM2 process manager configuration
└── README.md                       # Main documentation
```

## Building and Running

### Prerequisites

- **Python 3.13+**
- **Node.js v24+ LTS**
- **Qwen Code**
- **Obsidian v1.10.6+** (open the `Vault/` folder)
- **Git**

### Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install MCP servers
npm install -g @playwright/mcp

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials
```

### Running the System

```bash
# Start the orchestrator (main loop)
python src/orchestrator.py

# Run one cycle only (for testing)
python src/orchestrator.py --once

# Dry run (log actions but don't execute)
python src/orchestrator.py --dry-run

# Start the watchdog (monitors & auto-restarts watchers)
python src/watchdog.py

# Production: use PM2
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

### Configuration (`.env`)

Key environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `DEV_MODE` | `true` | Development mode (no real actions) |
| `DRY_RUN` | `true` | Log actions but don't execute |
| `VAULT_PATH` | `./Vault` | Path to Obsidian vault |
| `GMAIL_POLL_INTERVAL` | `60` | Seconds between Gmail polls |
| `WHATSAPP_POLL_INTERVAL` | `30` | Seconds between WhatsApp polls |
| `ORCHESTRATOR_CHECK_INTERVAL` | `30` | Seconds between orchestrator cycles |
| `WATCHDOG_CHECK_INTERVAL` | `30` | Seconds between watchdog checks |
| `PAYMENT_AUTO_APPROVE_UNDER` | `50` | USD threshold for auto-approval |
| `PAYMENT_REQUIRE_APPROVAL_OVER` | `100` | USD threshold requiring approval |

## Core Workflow

### Invoice Flow Example

1. **Detection**: WhatsApp Watcher detects "send invoice" message
2. **Create**: Action file in `Vault/Needs_Action/`
3. **Plan**: Orchestrator invokes Qwen Code → creates plan in `Vault/Plans/`
4. **Approve**: Approval request created in `Vault/Pending_Approval/` → human moves to `Approved/`
5. **Action**: Orchestrator executes via MCP servers
6. **Log**: Transaction recorded in `Vault/Logs/`, files moved to `Vault/Done/`

### Human-in-the-Loop Approval

Files in `Vault/Pending_Approval/` require manual action:
- **Approve**: Move file to `Vault/Approved/`
- **Reject**: Move file to `Vault/Rejected/`

Auto-approval rules are defined in `src/hitl.py` (`APPROVAL_THRESHOLDS`):
- Email to known contacts: auto-approve
- Payments < $50 (recurring, known payee): auto-approve
- File create/read/move within Vault: auto-approve
- Everything else: requires human approval

## Development Conventions

### Logging

- All components use the shared `utils.logger` module
- Log files: JSON format in `Vault/Logs/YYYY-MM-DD.log`
- Audit trail: JSONL format in `Vault/Logs/YYYY-MM-DD.jsonl`
- Log rotation: 10 MB max, 7 backups
- Console output: colorized, human-readable

### Testing

- Always test with `DRY_RUN=true` first
- Use `python src/orchestrator.py --once` for single-cycle testing
- Create test action files in `Vault/Needs_Action/` to trigger workflows

### Security

- **Never commit `.env`** — it's in `.gitignore`
- All credentials via environment variables
- Sensitive actions always require human approval
- Audit trail for every action (90-day retention minimum)

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed guides. Quick reference:

| Issue | Solution |
|-------|----------|
| Qwen Code not found | Install Qwen Code |
| Gmail API 403 | Enable API in Google Cloud, configure OAuth |
| Playwright MCP won't start | Kill existing processes, clear `/tmp/playwright-mcp-*` |
| Processes stop overnight | Use PM2: `pm2 start ecosystem.config.js` |
| High memory | Adjust polling intervals in `.env` |

## Key Files to Know

| File | Purpose |
|------|---------|
| `src/orchestrator.py` | Main loop — processes Needs_Action → Plans → Approval → Execution → Done |
| `src/watchdog.py` | Process monitor — auto-restarts failed watchers |
| `src/hitl.py` | Approval thresholds and request management |
| `src/utils/logger.py` | Shared logging (JSON files + colored console) |
| `Vault/Company_Handbook.md` | Business rules, rates, contact lists, escalation paths |
| `Vault/Dashboard.md` | Live status overview with placeholders (`{{TIMESTAMP}}`, etc.) |
| `ecosystem.config.js` | PM2 configuration for production deployment |
