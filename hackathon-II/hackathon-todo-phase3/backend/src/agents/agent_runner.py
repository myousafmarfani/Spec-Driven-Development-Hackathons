"""
OpenAI Agent Runner with Conversation History Support
This module runs the OpenAI agent with conversation history persistence.
"""
import os
import asyncio
import uuid
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlmodel import Session, select, func
import sys
import os
# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# Import using absolute imports from backend
from db import get_session
from src.models.conversation import Conversation
from src.models.message import Message, MessagePublic
from models import Task
from .todo_agent import TodoAgent


class AgentRunner:
    """
    Runs the OpenAI agent with conversation history support.
    Manages conversation state persistence in the database.
    """

    def __init__(self):
        self.agent = TodoAgent()

    def format_conversation_history(self, messages: List[Message]) -> List[Dict[str, str]]:
        """
        Format database messages into the format expected by the OpenAI API.

        Args:
            messages: List of Message objects from the database

        Returns:
            List of dictionaries in the format expected by OpenAI API
        """
        formatted_history = []

        for msg in messages:
            role = msg.role
            if role not in ['user', 'assistant', 'system']:
                # Default to user or assistant based on the content
                role = 'user'  # Default role if unknown

            formatted_history.append({
                "role": role,
                "content": msg.content
            })

        return formatted_history

    def get_conversation_history(self, conversation_id: int, db_session: Session) -> List[Dict[str, str]]:
        """
        Retrieve conversation history from the database.

        Args:
            conversation_id: ID of the conversation to retrieve
            db_session: Database session

        Returns:
            Formatted conversation history
        """
        # Query messages for this conversation, ordered by creation time
        statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at)
        results = db_session.exec(statement).all()

        return self.format_conversation_history(results)

    def run_agent_with_history(
        self,
        user_input: str,
        user_id: str,
        conversation_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Run the agent with conversation history support.

        Args:
            user_input: The user's natural language input
            user_id: The ID of the user
            conversation_id: Optional conversation ID to continue existing conversation

        Returns:
            Dictionary containing the agent's response and any tool calls made
        """
        import json

        # Get database session
        with next(get_session()) as db_session:
            # If no conversation_id provided, create a new conversation
            if not conversation_id:
                # Create a new conversation with a public UUID for external clients
                conversation = Conversation(
                    user_id=user_id,
                    conversation_id=str(uuid.uuid4())
                )
                db_session.add(conversation)
                db_session.commit()
                db_session.refresh(conversation)
                conversation_id = conversation.id
            else:
                # Try to get the existing conversation
                conversation = db_session.get(Conversation, conversation_id)
                if not conversation:
                    # If conversation doesn't exist, create a new one
                    conversation = Conversation(
                        user_id=user_id,
                        conversation_id=str(uuid.uuid4())
                    )
                    db_session.add(conversation)
                    db_session.commit()
                    db_session.refresh(conversation)
                    conversation_id = conversation.id

            # Get conversation history
            conversation_history = self.get_conversation_history(conversation_id, db_session)

            # Save user message to database
            user_message = Message(
                conversation_id=conversation_id,
                user_id=user_id,
                role="user",
                content=user_input
            )
            db_session.add(user_message)
            db_session.commit()

            # Run the agent with the conversation history
            result = self.agent.run_agent(
                user_input,
                user_id,
                conversation_history,
                metadata={"user_id": user_id}
            )

            # If there are tool calls, process them
            if result.get('tool_calls'):
                execution_messages = self._execute_tool_calls(
                    result['tool_calls'],
                    user_id,
                    db_session
                )

                # Combine execution summaries into a single assistant response
                final_response = "\n\n".join(msg for msg in execution_messages if msg)
                if not final_response:
                    final_response = "I attempted to run the requested action, but no result was returned."

                assistant_message = Message(
                    conversation_id=conversation_id,
                    user_id=user_id,
                    role="assistant",
                    content=final_response
                )
                db_session.add(assistant_message)
                db_session.commit()

                result['response'] = final_response
            elif result.get('response'):
                # If no tool calls were made, save the assistant response to database
                assistant_message = Message(
                    conversation_id=conversation_id,
                    user_id=user_id,
                    role="assistant",
                    content=result['response']
                )
                db_session.add(assistant_message)
                db_session.commit()

            # Add conversation_id to result
            result['conversation_id'] = conversation_id

            return result

    def _execute_tool_calls(self, tool_calls: List[Dict[str, Any]], user_id: str, db_session: Session) -> List[str]:
        """Execute each requested tool call and return human-readable summaries."""
        summaries: List[str] = []

        for tool_call in tool_calls:
            name = tool_call.get('name')
            raw_args = tool_call.get('arguments')

            try:
                if isinstance(raw_args, str):
                    args = json.loads(raw_args or "{}")
                elif isinstance(raw_args, dict):
                    args = raw_args
                else:
                    args = {}
            except json.JSONDecodeError:
                summaries.append(f"Could not understand arguments for {name}.")
                continue

            args['user_id'] = user_id

            try:
                summaries.append(self._execute_tool_call(name, args, db_session))
            except Exception as exc:
                summaries.append(f"Failed to run {name or 'tool'}: {exc}")

        return summaries

    def _execute_tool_call(self, name: Optional[str], args: Dict[str, Any], db_session: Session) -> str:
        """Execute a single tool call against the task data store."""
        if not name:
            raise ValueError("Tool name is required")

        user_id = args.get('user_id')
        now = datetime.utcnow()

        if name == 'add_task':
            title = args.get('title')
            if not title:
                raise ValueError("Missing task title")

            priority = (args.get('priority') or 'medium').lower()
            if priority not in {'low', 'medium', 'high'}:
                priority = 'medium'

            # Calculate the next task_number for this user
            max_task_number_query = select(func.max(Task.task_number)).where(Task.user_id == user_id)
            max_task_number = db_session.exec(max_task_number_query).first()
            next_task_number = (max_task_number or 0) + 1

            task = Task(
                title=title,
                description=args.get('description'),
                completed=False,
                priority=priority,
                due_date=self._parse_due_date(args.get('due_date')),
                user_id=user_id,
                task_number=next_task_number,
                created_at=now,
                updated_at=now
            )
            db_session.add(task)
            db_session.commit()
            db_session.refresh(task)

            return f"Added task #{task.task_number}: '{task.title}' (priority {task.priority})."

        if name == 'list_tasks':
            statement = select(Task).where(Task.user_id == user_id).order_by(Task.task_number.asc())
            tasks = db_session.exec(statement).all()
            if not tasks:
                return "You do not have any tasks yet."

            lines = []
            for task in tasks:
                status = 'done' if task.completed else 'pending'
                lines.append(f"[{status}] #{task.task_number} {task.title}")

            return "Here are your tasks:\n" + "\n".join(lines)

        if name == 'complete_task':
            task_id = args.get('task_id')
            task = self._get_task_for_user_by_number(task_id, user_id, db_session)
            task.completed = True
            task.updated_at = now
            db_session.add(task)
            db_session.commit()
            db_session.refresh(task)
            return f"Marked task #{task.task_number} '{task.title}' as completed."

        if name == 'delete_task':
            task_id = args.get('task_id')
            task = self._get_task_for_user_by_number(task_id, user_id, db_session)
            task_title = task.title
            task_number_value = task.task_number
            db_session.delete(task)
            db_session.commit()
            return f"Deleted task #{task_number_value} '{task_title}'."

        if name == 'update_task':
            task_id = args.get('task_id')
            task = self._get_task_for_user_by_number(task_id, user_id, db_session)

            updated_fields = []
            if 'title' in args and args['title']:
                task.title = args['title']
                updated_fields.append('title')
            if 'description' in args:
                task.description = args['description']
                updated_fields.append('description')
            if 'priority' in args and args['priority']:
                priority = args['priority'].lower()
                if priority in {'low', 'medium', 'high'}:
                    task.priority = priority
                    updated_fields.append('priority')
            if 'completed' in args and args['completed'] is not None:
                task.completed = bool(args['completed'])
                updated_fields.append('completed')
            if 'due_date' in args:
                task.due_date = self._parse_due_date(args['due_date'])
                updated_fields.append('due_date')

            if not updated_fields:
                return f"No valid updates were provided for task #{task.task_number}."

            task.updated_at = now
            db_session.add(task)
            db_session.commit()
            db_session.refresh(task)

            updated_list = ", ".join(updated_fields)
            return f"Updated task #{task.task_number} ({updated_list})."

        raise ValueError(f"Unsupported tool: {name}")

    def _get_task_for_user_by_number(self, task_number: Any, user_id: str, db_session: Session) -> Task:
        """Fetch a task by task_number ensuring it belongs to the user."""
        if task_number is None:
            raise ValueError("task_id/task_number is required")

        try:
            task_number_int = int(task_number)
        except (TypeError, ValueError):
            raise ValueError("task_id/task_number must be an integer")

        statement = select(Task).where(Task.user_id == user_id, Task.task_number == task_number_int)
        task = db_session.exec(statement).first()
        if not task:
            raise ValueError(f"Task #{task_number_int} not found for this user")

        return task

    def _get_task_for_user(self, task_id: Any, user_id: str, db_session: Session) -> Task:
        """Fetch a task by id ensuring it belongs to the user."""
        if task_id is None:
            raise ValueError("task_id is required")

        try:
            task_id_int = int(task_id)
        except (TypeError, ValueError):
            raise ValueError("task_id must be an integer")

        task = db_session.get(Task, task_id_int)
        if not task or task.user_id != user_id:
            raise ValueError("Task not found for this user")

        return task

    def _parse_due_date(self, due_date_value: Optional[str]) -> Optional[datetime]:
        """Parse ISO formatted due dates, returning None on failure."""
        if not due_date_value:
            return None

        if isinstance(due_date_value, datetime):
            return due_date_value

        try:
            normalized = due_date_value.replace('Z', '+00:00')
            return datetime.fromisoformat(normalized)
        except Exception:
            return None

    async def run_agent_async(
        self,
        user_input: str,
        user_id: str,
        conversation_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Async wrapper for running the agent with history support.
        """
        # Since the database operations are synchronous, we run them in a thread
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self.run_agent_with_history, user_input, user_id, conversation_id)
        return result