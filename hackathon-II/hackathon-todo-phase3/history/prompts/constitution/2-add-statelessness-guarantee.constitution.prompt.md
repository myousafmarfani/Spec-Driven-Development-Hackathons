---
id: 2
title: Add Statelessness Guarantee principle
stage: constitution
date: 2026-02-11
surface: agent
model: claude-sonnet-4-5-20250929
feature: constitution
branch: main
user: imher
command: Update constitution with statelessness principle
labels: [constitution,architecture,statelessness]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - specs/speckit.constitution.md
tests: []
---

## Prompt

Text from the user's message (preserved verbatim):
"but also did you add the stateless promise in the constitution?

I didn't see it - but if it's not there - let's add it."

## Response snapshot

Added Principle 3: "Statelessness Guarantee" to the constitution with these key requirements:
- Backend services must operate without in-memory state
- ALL state persists in database before responding
- Each request is completely independent
- Server can restart mid-conversation without data loss
- Enables horizontal scaling (any instance handles any request)

Forbidden practices explicitly listed:
- In-memory conversation caching
- Session-based state storage
- Redis/Memcached for conversation data
- Any state that doesn't survive server restart

Renumbered existing Principles 3-8 to 4-9.
Updated document version to 1.1.0.

## Outcome

- ✅ Impact: Added critical architectural principle ensuring stateless backend design for Phase 3 chatbot
- 🧪 Tests: N/A (constitutional amendment)
- 📁 Files: specs/speckit.constitution.md (1 file modified)
- 🔁 Next prompts: Update spec.md, plan.md, tasks.md to reference this principle; Update templates if needed
- 🧠 Reflection: Statelessness is a foundational architectural constraint that must be enforced throughout implementation

## Evaluation notes (flywheel)

- Failure modes observed: N/A
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Nothing - principle correctly defined. Verify downstream artifacts (spec/plan/tasks) explicitly reference this guarantee.
