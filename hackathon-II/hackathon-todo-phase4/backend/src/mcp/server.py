"""
MCP (Model Context Protocol) server implementation for todo management tools.
This server exposes 5 tools for task operations that call Phase 2 endpoints.
"""
import asyncio
import httpx
from typing import Dict, Any, List
from mcp.server import Server
from mcp.types import TextContent, Prompt, GetPromptResult, Tool, CallToolResult, ListPromptsResult
from urllib.parse import urljoin
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the base URL for the backend API
BASE_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000/api")

# Initialize the MCP server
server = Server("todo-mcp-server")


async def make_api_request(method: str, endpoint: str, user_id: str, json_data: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Helper function to make API requests to the Phase 2 backend endpoints.

    Args:
        method: HTTP method (GET, POST, PUT, PATCH, DELETE)
        endpoint: API endpoint path
        user_id: User ID for the request
        json_data: JSON payload for the request

    Returns:
        Response JSON data
    """
    full_url = urljoin(f"{BASE_API_URL}/{user_id}/", endpoint.lstrip('/'))

    async with httpx.AsyncClient() as client:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('FAKE_JWT_TOKEN', 'fake-jwt-token')}"  # In real implementation, this would be a proper JWT
        }

        if method.upper() == "GET":
            response = await client.get(full_url, headers=headers)
        elif method.upper() == "POST":
            response = await client.post(full_url, headers=headers, json=json_data)
        elif method.upper() == "PUT":
            response = await client.put(full_url, headers=headers, json=json_data)
        elif method.upper() == "PATCH":
            response = await client.patch(full_url, headers=headers, json=json_data)
        elif method.upper() == "DELETE":
            response = await client.delete(full_url, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        # Return the response data
        try:
            return response.json()
        except Exception:
            # If JSON parsing fails, return the text content
            return {"result": response.text, "status_code": response.status_code}


@server.list_prompts()
async def handle_list_prompts() -> ListPromptsResult:
    """List available prompts for the MCP server."""
    from mcp.types import PromptReference
    return ListPromptsResult(
        prompts=[
            PromptReference(
                name="todo-help",
                description="Get help with todo management commands"
            )
        ]
    )


@server.get_prompt()
async def handle_get_prompt(name: str) -> GetPromptResult:
    """Handle getting a specific prompt."""
    if name == "todo-help":
        return GetPromptResult(
            description="Todo Management Help",
            messages=[
                {
                    "role": "assistant",
                    "content": [
                        TextContent(
                            type="text",
                            text="Available commands: add_task, list_tasks, complete_task, delete_task, update_task"
                        )
                    ]
                }
            ]
        )

    # Raise a standard exception for unknown prompts
    raise ValueError(f"Unknown prompt: {name}")


@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available tools for task operations."""
    return [
        Tool(
            name="add_task",
            description="Add a new task for a user",
            inputSchema={
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
        ),
        Tool(
            name="list_tasks",
            description="List all tasks for a user",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "ID of the user"}
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="complete_task",
            description="Mark a task as completed",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "ID of the user"},
                    "task_id": {"type": "integer", "description": "ID of the task to complete"}
                },
                "required": ["user_id", "task_id"]
            }
        ),
        Tool(
            name="delete_task",
            description="Delete a task",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "ID of the user"},
                    "task_id": {"type": "integer", "description": "ID of the task to delete"}
                },
                "required": ["user_id", "task_id"]
            }
        ),
        Tool(
            name="update_task",
            description="Update a task",
            inputSchema={
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
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[CallToolResult]:
    """Handle tool calls for task operations."""
    try:
        if name == "add_task":
            # Extract arguments
            user_id = arguments["user_id"]
            title = arguments["title"]
            description = arguments.get("description", "")
            priority = arguments.get("priority", "medium")
            due_date = arguments.get("due_date")

            # Prepare payload for API request
            payload = {
                "title": title,
                "description": description,
                "priority": priority
            }

            if due_date:
                payload["due_date"] = due_date

            # Make API request to create task
            result = await make_api_request("POST", "tasks", user_id, payload)

            return [CallToolResult(content=[TextContent(type="text", text=f"Task added successfully: {result}")])]

        elif name == "list_tasks":
            user_id = arguments["user_id"]

            # Make API request to list tasks
            result = await make_api_request("GET", "tasks", user_id)

            if isinstance(result, list):
                tasks_str = "\n".join([f"- {task.get('title', 'No Title')} (ID: {task.get('id', 'N/A')})" for task in result])
                response_text = f"Tasks for user {user_id}:\n{tasks_str}" if result else f"No tasks found for user {user_id}"
            else:
                response_text = f"Tasks for user {user_id}: {result}"

            return [CallToolResult(content=[TextContent(type="text", text=response_text)])]

        elif name == "complete_task":
            user_id = arguments["user_id"]
            task_id = arguments["task_id"]

            # Make API request to update task (mark as completed)
            payload = {"completed": True}
            result = await make_api_request("PATCH", f"tasks/{task_id}", user_id, payload)

            return [CallToolResult(content=[TextContent(type="text", text=f"Task {task_id} marked as completed: {result}")])]

        elif name == "delete_task":
            user_id = arguments["user_id"]
            task_id = arguments["task_id"]

            # Make API request to delete task
            result = await make_api_request("DELETE", f"tasks/{task_id}", user_id)

            return [CallToolResult(content=[TextContent(type="text", text=f"Task {task_id} deleted: {result}")])]

        elif name == "update_task":
            user_id = arguments["user_id"]
            task_id = arguments["task_id"]

            # Prepare payload with provided arguments
            payload = {}
            if "title" in arguments:
                payload["title"] = arguments["title"]
            if "description" in arguments:
                payload["description"] = arguments["description"]
            if "completed" in arguments:
                payload["completed"] = arguments["completed"]
            if "priority" in arguments:
                payload["priority"] = arguments["priority"]
            if "due_date" in arguments:
                payload["due_date"] = arguments["due_date"]

            # Make API request to update task
            result = await make_api_request("PUT", f"tasks/{task_id}", user_id, payload)

            return [CallToolResult(content=[TextContent(type="text", text=f"Task {task_id} updated: {result}")])]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        # Return an error result instead of raising an exception
        return [CallToolResult(content=[TextContent(type="text", text=f"Error executing tool {name}: {str(e)}")])]
