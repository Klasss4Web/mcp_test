import logging
from core.mcp_client import MCPClient
from core.errors import AppException


class ProductService:
    def __init__(self):
        self.mcp = MCPClient()

    async def list_products(self):
        payload = {}
        try:
            products = await self.mcp.call_tool("list_products", payload)
            print(f"ProductService: Retrieved products: {products}")
            return products
        except Exception as e:
            logging.error(f"ProductService error: {str(e)}")
            raise AppException("Failed to list products")

    async def get_product(self, product_id: str = None, name: str = None):
        payload = {"product_id": product_id, "name": name}
        try:
            return await self.mcp.call_tool("get_product", payload)
        except Exception as e:
            logging.error(f"ProductService error: {str(e)}")
            raise AppException("Product lookup failed")

    async def search_products(self, query: str):
        payload = {"query": query}
        try:
            return await self.mcp.call_tool("search_products", payload)
        except Exception as e:
            logging.error(f"ProductService error: {str(e)}")
            raise AppException("Product search failed")
