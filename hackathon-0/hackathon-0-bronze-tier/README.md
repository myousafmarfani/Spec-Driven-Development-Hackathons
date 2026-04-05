# Personal AI Employee - Bronze Tier

> **Tagline:** Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.

A **Digital FTE (Full-Time Equivalent)** - an AI agent that works 24/7 to manage your personal and business affairs using Qwen Code as the reasoning engine and Obsidian as the local dashboard.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    PERSONAL AI EMPLOYEE                      │
└─────────────────────────────────────────────────────────────┘

External Sources → Watchers → Obsidian Vault → Qwen Code → MCP Servers → Actions
   (Gmail,           (Python    (Local         (Reasoning    (Email,       (Send Email,
    WhatsApp,        Scripts)    Markdown)      Engine)       Browser)       Post Social)
    Bank, Files)
                         ↓
                    Human-in-the-Loop Approval
```

## Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Brain** | Qwen Code | Reasoning engine |
| **Memory/GUI** | Obsidian | Local Markdown dashboard |
| **Senses** | Python Watchers | Monitor Gmail, WhatsApp, filesystem |
| **Hands** | MCP Servers | External actions (email, browser) |
| **Orchestration** | Python | Master process + watchdog |

## Quick Start

### Prerequisites

- **Python 3.13+**
- **Node.js v24+ LTS**
- **Qwen Code**
- **Obsidian v1.10.6+**
- **Git**

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd hackathon-0-bronze-tier

# Install Python dependencies
pip install -r requirements.txt

# Install MCP servers
npm install -g @playwright/mcp

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials

# Initialize Obsidian vault
# Open the Vault folder in Obsidian
```

### Project Structure

```
hackathon-0-bronze-tier/
├── Vault/                      # Obsidian vault (local-first knowledge base)
│   ├── Inbox/                  # Raw captures, notes, quick entries
│   ├── Needs_Action/           # Incoming triggers from watchers
│   ├── Plans/                  # Qwen-generated action plans
│   ├── Pending_Approval/       # Awaiting human approval
│   ├── Approved/               # Ready for execution
│   ├── Rejected/               # Declined actions
│   ├── Done/                   # Completed tasks
│   ├── Logs/                   # Audit logs
│   ├── Invoices/               # Generated invoices
│   ├── Agents/                 # Agent configurations
│   ├── Dashboard.md            # Main dashboard
│   ├── Company_Handbook.md     # Rules and guidelines
│   └── Business_Goals.md       # Objectives and metrics
├── src/                        # Python source code
│   ├── orchestrator.py         # Master process
│   ├── watchdog.py             # Health monitor
│   ├── watchers/               # Sentinel scripts
│   │   ├── gmail_watcher.py
│   │   ├── whatsapp_watcher.py
│   │   └── file_watcher.py
│   ├── mcp/                    # MCP client integrations
│   │   ├── email_mcp.py
│   │   └── browser_mcp.py
│   └── utils/                  # Utilities
│       ├── logger.py
│       └── hitl.py
├── scripts/                    # Helper scripts
├── .env.example                # Environment template
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Core Features

### 1. Watchers (Perception Layer)

Lightweight Python scripts that continuously monitor external sources:

- **Gmail Watcher**: Detects new emails matching triggers
- **WhatsApp Watcher**: Monitors WhatsApp messages (via Playwright)
- **File Watcher**: Watches filesystem for changes
- **Finance Watcher**: Monitors bank transactions

### 2. Human-in-the-Loop (HITL)

Safety-first approval system:

| Action Category | Auto-Approve | Require Approval |
|-----------------|--------------|------------------|
| Email replies | Known contacts | New contacts, bulk |
| Payments | < $50 recurring | New payees, > $100 |
| Social media | Scheduled posts | Replies, DMs |
| File operations | Create, read | Delete, move |

### 3. Audit Logging

Every action is logged for review:

```json
{
  "timestamp": "2026-01-07T10:30:00Z",
  "action_type": "email_send",
  "actor": "qwen_code",
  "target": "client@example.com",
  "approval_status": "approved",
  "result": "success"
}
```

## Usage

### Start the System

```bash
# Start all watchers and orchestrator
python src/orchestrator.py

# Or use PM2 for production (recommended)
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

### Daily Workflow

1. **Morning**: Check `Vault/Dashboard.md` for overnight activity
2. **Review**: Move files from `Pending_Approval/` to `Approved/` or `Rejected/`
3. **Monitor**: Check `Vault/Logs/` for any issues

### Example: Invoice Flow

1. **Detection**: WhatsApp Watcher detects "send invoice" message
2. **Create**: `/Vault/Needs_Action/WHATSAPP_client_2026-01-07.md`
3. **Plan**: Qwen creates `/Vault/Plans/PLAN_invoice_client.md`
4. **Approve**: You review and move to `/Approved/`
5. **Action**: Email MCP sends invoice
6. **Log**: Transaction recorded in `/Vault/Logs/`

## Security

### Credential Management

- **Never commit** `.env` files
- Use environment variables for all secrets
- Rotate credentials regularly
- Enable 2FA on all accounts

### Sandboxing

```bash
# Development mode (no real actions)
export DEV_MODE=true
export DRY_RUN=true

# Run with dry-run flag
python src/orchestrator.py --dry-run
```

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues.

## Hackathon Submission

- **Tier**: Bronze
- **GitHub**: [Your Repository]
- **Demo Video**: [5-10 minute walkthrough]
- **Submit Form**: https://forms.gle/JR9T1SJq5rmQyGkGA

## License

MIT License - See LICENSE file for details.

## Resources

- [Qwen Code Documentation](https://agentfactory.panaversity.org/docs/AI-Tool-Landscape/claude-code-features-and-workflows)
- [MCP Introduction](https://modelcontextprotocol.io/introduction)
- [Obsidian Help](https://help.obsidian.md/Getting+started)
- [Playwright Docs](https://playwright.dev/python/docs/intro)
