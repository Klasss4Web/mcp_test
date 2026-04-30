import httpx
import logging
from core.config import get_settings
from core.errors import AppException

class MCPClient:
    def __init__(self):
        self.settings = get_settings()
        self.base_url = self.settings.MCP_SERVER_URL # Should be the base /mcp URL
        # It's better to use a context manager or a managed client to avoid leaking connections
        self.client = httpx.AsyncClient()

    async def call_tool(self, tool: str, arguments: dict):
        # 1. ALWAYS hit the base URL. Do not append /{tool}
        url = self.base_url 
        
        # 2. Wrap the request in the JSON-RPC 2.0 format required by MCP
        json_rpc_payload = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "tools/call",
            "params": {
                "name": tool,
                "arguments": arguments
            }
        }

        # 3. Add the mandatory headers we discovered earlier
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        try:
            response = await self.client.post(
                url, 
                json=json_rpc_payload, 
                headers=headers, 
                timeout=15
            )
            
            # 4. Handle errors gracefully
            if response.status_code != 200:
                logging.error(f"MCP Server Error: {response.status_code} - {response.text}")
                raise AppException(f"MCP service error: {response.status_code}", status_code=response.status_code)

            return response.json()

        except httpx.HTTPStatusError as e:
            logging.error(f"MCP HTTP error: {e.response.status_code} {e.response.text}")
            raise AppException(f"MCP error: {e.response.text}", status_code=e.response.status_code)
        except Exception as e:
            logging.error(f"MCP connection error: {str(e)}")
            raise AppException("Could not connect to Meridian backend services")