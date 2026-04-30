import logging
from core.mcp_client import MCPClient
from core.errors import AppException

class ProductService:
    def __init__(self):
        self.mcp = MCPClient()

    async def list_products(self, limit: int = 20):
        """Retrieves a list of available products."""
        try:
            # MCP tools expect a dict for arguments
            return await self.mcp.call_tool("list_products", {"limit": limit})
        except Exception as e:
            logging.error(f"ProductService error: {str(e)}")
            raise AppException("Failed to list products")

    async def search_products(self, query: str):
        """Searches the catalog for products matching the given query."""
        try:
            return await self.mcp.call_tool("search_products", {"query": query})
        except Exception as e:
            logging.error(f"ProductService error: {str(e)}")
            raise AppException("Product search failed")