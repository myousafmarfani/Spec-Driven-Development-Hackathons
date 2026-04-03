"""
MCP Package Entry Point
This module allows running the MCP server as an SSE transport over HTTP.
"""

import asyncio
import os
import sys

# Add the backend directory to the path so we can import backend modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from dotenv import load_dotenv
load_dotenv()

import uvicorn
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.responses import JSONResponse
from mcp.server.sse import SseServerTransport

from .server import server

# Create SSE transport
sse = SseServerTransport("/messages/")


async def handle_sse(request):
    """Handle SSE connections from MCP clients."""
    async with sse.connect_sse(request.scope, request.receive, request._send) as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


async def health(request):
    return JSONResponse({"status": "healthy", "service": "mcp-server"})


# Build Starlette app
app = Starlette(
    debug=True,
    routes=[
        Route("/health", health),
        Route("/sse", endpoint=handle_sse),
        Mount("/messages/", app=sse.handle_post_message),
    ],
)


def main():
    """Main function to start the MCP server."""
    host = os.getenv("MCP_SERVER_HOST", "localhost")
    port = int(os.getenv("MCP_SERVER_PORT", "8001"))

    print(f"Starting MCP SSE server on http://{host}:{port}")
    print("  SSE endpoint: /sse")
    print("  Messages endpoint: /messages/")
    print("Available tools: add_task, list_tasks, complete_task, delete_task, update_task")

    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()