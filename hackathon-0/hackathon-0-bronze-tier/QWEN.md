# Personal AI Employee - Bronze Tier

> **Hackathon 0: Building Autonomous FTEs in 2026**  
> **Tagline:** Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.

---

## Project Overview

This is a **complete Bronze Tier implementation** of the Personal AI Employee hackathon. It creates a **Digital FTE (Full-Time Equivalent)** - an AI agent that works 24/7 to manage personal and business affairs using:

- **Claude Code** as the reasoning engine
- **Obsidian** as the local Markdown dashboard
- **Python Watchers** for Gmail, WhatsApp, and filesystem monitoring
- **MCP Servers** for browser automation and external actions
- **Human-in-the-Loop (HITL)** approval system for safety

---

## Directory Structure

```
hackathon-0-bronze-tier/
├── Vault/                          # Obsidian vault (local-first knowledge base)
│   ├── Needs_Action/               # Incoming triggers from watchers
│   ├── Plans/                      # Claude-generated action plans
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
│   ├── orchestrator.py             # Master process
│   ├── watchdog.py                 # Health monitor
│   ├── hitl.py                     # Human-in-the-Loop system
│   ├── watchers/                   # Sentinel scripts
│   │   ├── gmail_watcher.py
│   │   ├── whatsapp_watcher.py
│   │   └── file_watcher.py
│   ├── mcp/                        # MCP client integrations
│   │   └── email_mcp.py
│   └── utils/                      # Utilities
│       └── logger.py
├── .qwen/                          # Qwen skills (browser automation)
│   └── skills/
│       └── browsing-with-playwright/
├── scripts/                        # Helper scripts
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
├── ecosystem.config.js             # PM2 process configuration
├── requirements.txt                # Python dependencies
├── README.md                       # Main documentation
├── SECURITY.md                     # Security best practices
├── TROUBLESHOOTING.md              # Common issues and solutions
└── DEMO.md                         # End-to-end demo walkthrough
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PERSONAL AI EMPLOYEE                      │
└─────────────────────────────────────────────────────────────┘

External Sources → Watchers → Obsidian Vault → Claude Code → MCP Servers → Actions
   (Gmail,           (Python    (Local         (Reasoning    (Email,       (Send Email,
    WhatsApp,        Scripts)    Markdown)      Engine)       Browser)       Post Social)
    Bank, Files)
                         ↓
                    Human-in-the-Loop Approval
```

### Components

| Layer | Component | Purpose |
|-------|-----------|---------|
| **Perception** | Gmail/WhatsApp/File Watchers | Monitor external triggers |
| **Memory** | Obsidian Vault | Local Markdown storage |
| **Reasoning** | Claude Code | Analysis and planning |
| **Action** | MCP Servers | External integrations |
| **Safety** | HITL System | Human approval workflow |
| **Health** | Watchdog | Process monitoring |
| **Control** | Orchestrator | Master coordination |

---

## Quick Start

### Prerequisites

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.13+ | Core runtime |
| Node.js | v24+ LTS | MCP servers |
| Claude Code | Latest | AI reasoning |
| Obsidian | v1.10.6+ | Dashboard |
| Git | Latest | Version control |

### Installation

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Install Playwright MCP
npm install -g @playwright/mcp

# 3. Set up environment
cp .env.example .env
# Edit .env with your credentials

# 4. Configure Claude Code
claude  # Run interactive setup

# 5. Open vault in Obsidian
# File → Open Folder → Select Vault/
```

### Start the System

```bash
# Option A: Using PM2 (recommended for production)
npm install -g pm2
pm2 start ecosystem.config.js
pm2 save
pm2 startup

# Option B: Manual (for testing)
python src/orchestrator.py
python src/watchdog.py
```

---

## Core Features

### 1. Watchers (Perception Layer)

**Gmail Watcher** (`src/watchers/gmail_watcher.py`)
- Polls Gmail API every 60 seconds
- Detects trigger keywords: invoice, payment, meeting, urgent
- Creates action files in `Vault/Needs_Action/`

**WhatsApp Watcher** (`src/watchers/whatsapp_watcher.py`)
- Uses Playwright MCP for WhatsApp Web
- Detects messages with trigger keywords
- Requires browser MCP server running

**File Watcher** (`src/watchers/file_watcher.py`)
- Monitors `Vault/Incoming/` and `Vault/Approved/`
- Uses watchdog library for real-time detection
- Triggers on file creation/modification

### 2. Orchestrator (`src/orchestrator.py`)

The master process that:
1. Polls `Vault/Needs_Action/` for new tasks
2. Invokes Claude Code to create plans
3. Creates approval requests in `Vault/Pending_Approval/`
4. Executes approved actions from `Vault/Approved/`
5. Moves completed tasks to `Vault/Done/`
6. Updates `Vault/Dashboard.md`

### 3. Watchdog (`src/watchdog.py`)

Health monitor that:
- Tracks all process PIDs
- Auto-restarts failed processes
- Alerts on repeated failures
- Updates dashboard with system health

### 4. HITL System (`src/hitl.py`)

Human-in-the-Loop management:
- Creates approval requests
- Enforces approval thresholds
- Tracks approval status
- Maintains audit trail

**Approval Thresholds:**

| Action | Auto-Approve | Require Approval |
|--------|--------------|------------------|
| Email to known contact | ✓ | |
| Email to new contact | | ✓ |
| Payment < $50 (recurring) | ✓ | |
| Payment > $100 | | ✓ |
| File create/read | ✓ | |
| File delete | | ✓ |

### 5. MCP Integration (`src/mcp/`)

**Email MCP:**
- Sends emails via Gmail web interface
- Uses Playwright for browser automation
- Supports attachments

**Browser MCP:**
- Navigation, snapshots, screenshots
- Form filling, clicking, typing
- JavaScript evaluation

---

## Usage

### Daily Workflow

1. **Morning Check** (2 minutes)
   - Open `Vault/Dashboard.md` in Obsidian
   - Review overnight activity
   - Check pending approvals

2. **Approval Review** (as needed)
   - Navigate to `Vault/Pending_Approval/`
   - Review each request
   - Move to `Approved/` or `Rejected/`

3. **Evening Review** (5 minutes)
   - Check `Vault/Done/` for completed tasks
   - Review `Vault/Logs/` for errors
   - Update `Vault/Business_Goals.md` progress

### Testing

```bash
# Test in dry-run mode (no real actions)
export DRY_RUN=true
export DEV_MODE=true

# Run orchestrator once
python src/orchestrator.py --once

# Check process status
python src/watchdog.py --status

# View logs
tail -f Vault/Logs/*.log
```

---

## Demo: Invoice Flow

See `DEMO.md` for complete walkthrough. Summary:

1. **Client sends WhatsApp**: "Send invoice for January"
2. **WhatsApp Watcher detects** → Creates action file
3. **Orchestrator invokes Claude** → Creates plan
4. **HITL creates approval** → Waits for human
5. **Human approves** → Moves to Approved folder
6. **Orchestrator executes** → Sends email with invoice
7. **Transaction logged** → Audit trail complete

**Timeline:** ~6 minutes (mostly waiting for human approval)

---

## Security

### Credential Management

```bash
# NEVER commit .env
echo ".env" >> .gitignore

# Use environment variables
export GMAIL_CLIENT_ID=xxx
export BANK_API_TOKEN=xxx
```

### Sandboxing

```bash
# Development mode
export DRY_RUN=true
export DEV_MODE=true

# Test without real actions
python src/orchestrator.py --dry-run
```

### Audit Logging

All actions logged to `Vault/Logs/`:
```json
{
  "timestamp": "2026-01-07T10:30:00Z",
  "action_type": "email_send",
  "target": "client@example.com",
  "approval_status": "approved",
  "result": "success"
}
```

See `SECURITY.md` for complete security guide.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Claude not found | `npm install -g @anthropic/claude-code` |
| Gmail 403 error | Enable Gmail API in Google Cloud Console |
| MCP server won't start | `bash scripts/start-server.sh` |
| Watchers stop overnight | Use PM2: `pm2 start ecosystem.config.js` |
| High memory usage | Adjust polling intervals in `.env` |

See `TROUBLESHOOTING.md` for complete troubleshooting guide.

---

## Hackathon Submission

### Checklist

- [ ] GitHub repository with all code
- [ ] README.md with setup instructions
- [ ] Demo video (5-10 minutes)
- [ ] Security disclosure
- [ ] Submit form: https://forms.gle/JR9T1SJq5rmQyGkGA

### Judging Criteria

| Criterion | Weight |
|-----------|--------|
| Functionality | 30% |
| Innovation | 25% |
| Practicality | 20% |
| Security | 15% |
| Documentation | 10% |

---

## Files Reference

### Documentation

| File | Purpose |
|------|---------|
| `README.md` | Main documentation |
| `DEMO.md` | End-to-end demo walkthrough |
| `SECURITY.md` | Security best practices |
| `TROUBLESHOOTING.md` | Common issues |
| `QWEN.md` | This file - project context |

### Vault Files

| File | Purpose |
|------|---------|
| `Vault/Dashboard.md` | System dashboard |
| `Vault/Company_Handbook.md` | AI rules and guidelines |
| `Vault/Business_Goals.md` | Objectives and metrics |

### Source Code

| File | Purpose |
|------|---------|
| `src/orchestrator.py` | Master coordination |
| `src/watchdog.py` | Health monitor |
| `src/hitl.py` | Human-in-the-Loop |
| `src/watchers/*.py` | Sentinel scripts |
| `src/mcp/*.py` | MCP integrations |
| `src/utils/logger.py` | Logging utility |

### Configuration

| File | Purpose |
|------|---------|
| `.env.example` | Environment template |
| `requirements.txt` | Python dependencies |
| `ecosystem.config.js` | PM2 configuration |
| `.gitignore` | Git ignore rules |

---

## Resources

- [Claude Code Docs](https://agentfactory.panaversity.org/docs/AI-Tool-Landscape/claude-code-features-and-workflows)
- [MCP Introduction](https://modelcontextprotocol.io/introduction)
- [Obsidian Help](https://help.obsidian.md/)
- [Playwright Docs](https://playwright.dev/)
- [Hackathon PDF](Personal%20AI%20Employee%20Hackathon%200_%20Building%20Autonomous%20FTEs%20in%202026.pdf)

---

## Version

- **Tier:** Bronze
- **Version:** 1.0.0
- **Last Updated:** 2026-01-07

---

**Built for Hackathon 0: Building Autonomous FTEs in 2026**
