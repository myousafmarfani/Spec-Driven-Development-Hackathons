"""
OpenAI Todo Agent Configuration
This module sets up the OpenAI agent with MCP tools for todo management.
"""
import os
import sys
from dotenv import load_dotenv
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from openai import OpenAI

# Load environment variables from backend/.env
backend_dir = os.path.join(os.path.dirname(__file__), '..', '..')
env_path = os.path.join(backend_dir, '.env')
load_dotenv(env_path)


class TodoAgent:
    """
    Todo Agent that uses OpenAI API with OpenRouter fallback for task management.
    """

    def __init__(self):
        # Primary: OpenAI configuration
        self.primary_api_key = os.getenv("OPENAI_API_KEY")
        self.primary_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.primary_base_url = None  # Use default OpenAI base URL
        
        # Fallback: OpenRouter configuration
        self.fallback_api_key = os.getenv("OPENROUTER_API_KEY")
        self.fallback_model = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-exp:free")
        self.fallback_base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        
        # Check if at least one API key is available
        if not self.primary_api_key and not self.fallback_api_key:
            raise RuntimeError("Neither OPENAI_API_KEY nor OPENROUTER_API_KEY found in environment variables")
        
        # Initialize clients (will be created on demand)
        self.primary_client = None
        self.fallback_client = None
        self.current_provider = None  # Track which provider is being used
        
        # Initialize primary client if available
        if self.primary_api_key:
            try:
                self.primary_client = OpenAI(api_key=self.primary_api_key)
                self.current_provider = "OpenAI"
                print(f"✓ Primary provider (OpenAI) initialized successfully")
            except Exception as e:
                print(f"⚠ Failed to initialize primary provider (OpenAI): {str(e)}")
        
        # Initialize fallback client if available
        if self.fallback_api_key:
            try:
                self.fallback_client = OpenAI(
                    api_key=self.fallback_api_key,
                    base_url=self.fallback_base_url
                )
                if not self.current_provider:
                    self.current_provider = "OpenRouter"
                print(f"✓ Fallback provider (OpenRouter) initialized successfully")
            except Exception as e:
                print(f"⚠ Failed to initialize fallback provider (OpenRouter): {str(e)}")
        
        if not self.primary_client and not self.fallback_client:
            raise RuntimeError("Failed to initialize any AI provider")

        # Define the tools that the agent can use
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Add a new task for a user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "ID of the user"},
                            "title": {"type": "string", "description": "Title of the task"},
                            "description": {"type": "string", "description": "Description of the task"},
                            "priority": {"type": "string", "description": "Priority of the task (low, medium, high)"},
                            "due_date": {"type": "string", "description": "Due date in ISO format"}
                        },
                        "required": ["user_id", "title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List all tasks for a user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "ID of the user"}
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as completed",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "ID of the user"},
                            "task_id": {"type": "integer", "description": "ID of the task to complete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "ID of the user"},
                            "task_id": {"type": "integer", "description": "ID of the task to delete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update a task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "ID of the user"},
                            "task_id": {"type": "integer", "description": "ID of the task to update"},
                            "title": {"type": "string", "description": "New title of the task"},
                            "description": {"type": "string", "description": "New description of the task"},
                            "completed": {"type": "boolean", "description": "Whether the task is completed"},
                            "priority": {"type": "string", "description": "New priority of the task (low, medium, high)"},
                            "due_date": {"type": "string", "description": "New due date in ISO format"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            }
        ]

    def run_agent(
        self,
        user_input: str,
        user_id: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Run the agent with user input and return the response.

        Args:
            user_input: The user's natural language input
            user_id: The ID of the user
            conversation_history: Previous conversation history

        Returns:
            Dictionary containing the agent's response and any tool calls made
        """
        # Prepare messages for the API call
        messages = []

        # Add system message to guide the agent
        system_message = (
            "You are an AI todo assistant for the Phase 3 MVP. "
            "Use only the provided tools (add_task, list_tasks, complete_task, delete_task, update_task) to fulfill user requests. "
            "Ask follow-up questions only when critical details (like task title or task id) are missing. "
            "If the user does not mention optional fields such as description, priority, or due date, proceed with sensible defaults instead of asking. "
            "After executing the necessary tools, respond with a concise summary of what happened and the resulting task state. "
            "Do not ask the user for internal identifiers or implementation details."
        )

        if metadata and metadata.get("user_id"):
            system_message += (
                f" The authenticated user id is {metadata['user_id']}. Always include this value automatically when calling tools and never ask the user for it."
            )

        messages.append({
            "role": "system",
            "content": system_message
        })

        # Add conversation history if provided
        if conversation_history:
            for msg in conversation_history:
                messages.append(msg)

        # Add the current user message
        messages.append({"role": "user", "content": user_input})

        # Try primary provider first, then fallback
        providers = []
        if self.primary_client:
            providers.append(("OpenAI", self.primary_client, self.primary_model))
        if self.fallback_client:
            providers.append(("OpenRouter", self.fallback_client, self.fallback_model))
        
        last_error = None
        
        for provider_name, client, model in providers:
            try:
                print(f"🔄 Attempting request with {provider_name}...")
                
                # Make the API call with tools
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    tools=self.tools,
                    tool_choice="auto"
                )

                # If successful, update current provider
                self.current_provider = provider_name
                print(f"✓ Request successful with {provider_name}")

                # Process the response
                response_message = response.choices[0].message
                tool_calls = response_message.tool_calls

                # If the model wants to call tools
                if tool_calls:
                    return {
                        "response": response_message.content or "",
                        "tool_calls": [
                            {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            } for tc in tool_calls
                        ],
                        "finish_reason": response.choices[0].finish_reason,
                        "provider": provider_name
                    }
                else:
                    # If no tool calls were made, return the content directly
                    return {
                        "response": response_message.content or "",
                        "tool_calls": [],
                        "finish_reason": response.choices[0].finish_reason,
                        "provider": provider_name
                    }

            except Exception as e:
                import traceback
                last_error = e
                print(f"\n⚠ {provider_name} API ERROR")
                print(f"Error type: {type(e).__name__}")
                print(f"Error message: {str(e)}")
                
                # If this isn't the last provider, try the next one
                if provider_name != providers[-1][0]:
                    print(f"→ Falling back to next provider...\n")
                    continue
                else:
                    # This was the last provider, show full trace
                    traceback.print_exc()
                    print(f"======================\n")
        
        # All providers failed
        return {
            "response": f"Sorry, all AI providers failed. Last error: {str(last_error)}",
            "tool_calls": [],
            "error": str(last_error)
        }