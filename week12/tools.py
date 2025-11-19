from langchain_core.tools import tool
from langchain_mcp_adapters.client import MultiServerMCPClient
from typing import Dict, Any, Optional
import asyncio

client = MultiServerMCPClient(  
    {
        "comfyui": {
            "transport": "streamable_http",  # HTTP-based remote server
            # Ensure you start your mcp server before running this code
            # cd to week12/comfyui-mcp-server and run: python server.py
            "url": "http://localhost:8000/mcp",
        }
    }
)

tools = asyncio.run(client.get_tools())  # type: Dict[str, Any]