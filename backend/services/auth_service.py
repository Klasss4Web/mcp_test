import logging
from core.mcp_client import MCPClient
from core.errors import AppException


class AuthService:
    def __init__(self):
        self.mcp = MCPClient()

    async def get_customer(self, email: str):
        payload = {"email": email}
        try:
            return await self.mcp.call_tool("get_customer", payload)
        except Exception as e:
            logging.error(f"AuthService error: {str(e)}")
            raise AppException("Customer lookup failed")

    async def verify_customer_pin(self, customer_id: str, pin: str):
        payload = {"customer_id": customer_id, "pin": pin}
        try:
            return await self.mcp.call_tool("verify_customer_pin", payload)
        except Exception as e:
            logging.error(f"AuthService error: {str(e)}")
            raise AppException("PIN verification failed")
