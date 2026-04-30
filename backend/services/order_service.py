import logging
from core.mcp_client import MCPClient
from core.errors import AppException


class OrderService:
    def __init__(self):
        self.mcp = MCPClient()

    async def list_orders(self, customer_id: str):
        payload = {"customer_id": customer_id}
        try:
            return await self.mcp.call_tool("list_orders", payload)
        except Exception as e:
            logging.error(f"OrderService error: {str(e)}")
            raise AppException("Failed to list orders")

    async def get_order(self, order_id: str):
        payload = {"order_id": order_id}
        try:
            return await self.mcp.call_tool("get_order", payload)
        except Exception as e:
            logging.error(f"OrderService error: {str(e)}")
            raise AppException("Failed to get order details")

    async def create_order(self, customer_id: str, product_id: str, quantity: int):
        payload = {"customer_id": customer_id, "product_id": product_id, "quantity": quantity}
        try:
            return await self.mcp.call_tool("create_order", payload)
        except Exception as e:
            logging.error(f"OrderService error: {str(e)}")
            raise AppException("Order placement failed")
