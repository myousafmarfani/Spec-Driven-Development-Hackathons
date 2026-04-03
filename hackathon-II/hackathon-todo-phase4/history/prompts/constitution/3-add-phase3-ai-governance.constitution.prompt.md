---
id: 3
title: Add Phase 3 AI chatbot governance principles
stage: constitution
date: 2026-02-12
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: MYousuf-Codes
command: sp.constitution
labels: ["constitution", "governance", "ai", "mcp", "phase3"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - null
---

## Prompt

UPDATE: Add Phase 3 AI chatbot governance principles:

AI & MCP ARCHITECTURE:
- All MCP tools MUST be stateless and database-backed
- Conversation state MUST persist to Neon DB (no in-memory state)
- Agent responses MUST confirm actions explicitly
- MCP tools MUST validate user_id before any operation
- Chat endpoint MUST be stateless (fetch history → process → store → respond)

OPENAI INTEGRATION:
- Use OpenAI Agents SDK for AI logic
- Use Official MCP SDK for tool exposure
- ChatKit requires domain allowlist configuration before deployment
- JWT tokens from Better Auth required for all chat endpoints

ERROR HANDLING:
- MCP tools gracefully handle task not found errors
- Agent provides friendly error messages to users
- Failed tool calls logged but don't crash conversation

## Response snapshot

Updated constitution to version 1.2.0 by adding three new principles:
- Principle 10: AI & MCP Architecture (stateless, database-backed, user validation)
- Principle 11: OpenAI Integration (official SDKs, domain allowlists, JWT auth)
- Principle 12: Error Handling & Resilience (graceful failures, user-friendly messages)

All placeholders in the template were filled with concrete values from the existing constitution and new governance rules. Version was bumped from 1.1.0 to 1.2.0 (MINOR increment for new principles). Sync Impact Report included at top of file.

## Outcome

- ✅ Impact: Constitution updated with Phase 3 AI governance rules, aligned with existing principles 1-9
- 🧪 Tests: No tests applicable (documentation update)
- 📁 Files: .specify/memory/constitution.md (updated)
- 🔁 Next prompts: Update README.md to document AI/chatbot architecture; verify Neon DB schema supports conversation tables; configure OpenAI domain allowlist
- 🧠 Reflection: Successfully integrated new AI governance principles while maintaining consistency with existing constitution structure. All placeholders resolved.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PENDING
- Prompt variant (if applicable): standard
- Next experiment (smallest change to try): N/A
