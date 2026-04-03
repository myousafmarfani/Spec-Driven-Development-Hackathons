# Prompt History Record

## Prompt
Phase 3: AI Chatbot for Todo Management

USER STORIES:
- As a user, I can chat with an AI to manage my todos using natural language
- As a user, I can say 'add task buy groceries' and it creates the task
- As a user, I can ask 'what's pending?' and see incomplete tasks
- As a user, I can say 'mark task 3 complete' and it updates the task
- As a user, I can say 'delete the meeting task' and it removes it
- As a user, conversations persist after server restarts

REQUIREMENTS:
- ChatKit UI on /chat route for conversational interface
- POST /api/{user_id}/chat endpoint (stateless, JWT-protected)
- MCP server: add_task, list_tasks, complete_task, delete_task, update_task
- OpenAI Agents SDK integration with MCP tools
- Database models: Conversation, Message (extend existing Task model)
- Natural language understanding for task operations

ACCEPTANCE CRITERIA:
- Chatbot understands 8 natural language commands
- All task operations work via chat
- Conversation history persists across sessions
- Server holds no state

## Response
[Claude's response to the user's prompt]

## Metadata
- ID: 5
- Stage: spec
- Date: 2026-02-12
- Model: sonnet
- Surface