#!/usr/bin/env python3
"""Main MCP Server"""

import asyncio
from mcp.server import Server
from mcp.types import Tool, TextContent, ToolResult

from my_mcp.tools.calculator import add, subtract
from my_mcp.tools.text_tools import reverse_text, uppercase_text
from my_mcp.resources.data import get_sample_data

# Initialize server
server = Server("my-mcp-server")


@server.call_tool()
async def handle_tool_call(name: str, arguments: dict) -> ToolResult:
    """Route tool calls to appropriate handlers"""

    if name == "add":
        result = add(arguments["a"], arguments["b"])
        text = f"{arguments['a']} + {arguments['b']} = {result}"

    elif name == "subtract":
        result = subtract(arguments["a"], arguments["b"])
        text = f"{arguments['a']} - {arguments['b']} = {result}"

    elif name == "reverse_text":
        result = reverse_text(arguments["text"])
        text = f"Reversed: {result}"

    elif name == "uppercase_text":
        result = uppercase_text(arguments["text"])
        text = f"Uppercase: {result}"

    else:
        return ToolResult(
            content=[TextContent(type="text", text=f"Unknown tool: {name}")],
            is_error=True,
        )

    return ToolResult(
        content=[TextContent(type="text", text=text)],
        is_error=False,
    )


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools"""
    return [
        Tool(
            name="add",
            description="Add two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
        ),
        Tool(
            name="subtract",
            description="Subtract two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
        ),
        Tool(
            name="reverse_text",
            description="Reverse a string",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to reverse"},
                },
                "required": ["text"],
            },
        ),
        Tool(
            name="uppercase_text",
            description="Convert text to uppercase",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to convert"},
                },
                "required": ["text"],
            },
        ),
    ]


@server.list_resources()
async def list_resources():
    """List available resources"""
    return [
        {
            "uri": "data://sample",
            "name": "Sample Data",
            "description": "Sample JSON data",
            "mimeType": "application/json",
        }
    ]


@server.read_resource()
async def read_resource(uri: str):
    """Read resource content"""
    if uri == "data://sample":
        data = get_sample_data()
        return TextContent(type="text", text=str(data))
    return TextContent(type="text", text="Resource not found", is_error=True)


async def main():
    """Run the server"""
    async with server:
        await server.wait_for_shutdown()


if __name__ == "__main__":
    asyncio.run(main())