import logging
from core.mcp_client import MCPClient
from core.errors import AppException

class ChatService:
    def __init__(self):
        self.mcp = MCPClient()

    async def chat(self, user_id: str, message: str):
        payload = {"user_id": user_id, "message": message}
        try:
            result = await self.mcp.call_tool("chat", payload)
            return result
        except Exception as e:
            logging.error(f"ChatService error: {str(e)}")
            raise AppException("Failed to process chat request")
