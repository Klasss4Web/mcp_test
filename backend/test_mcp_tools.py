import asyncio
import httpx
import os
import json

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "https://order-mcp-74afyau24q-uc.a.run.app/mcp")

# Added Content-Type to ensure the server accepts the JSON payload
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

async def call_tool(tool_name, tool_args, request_id=1):
    """
    Standard MCP tool call wrapper via JSON-RPC
    """
    payload = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": tool_args
        }
    }
    
    async with httpx.AsyncClient(timeout=20.0) as client:
        try:
            response = await client.post(MCP_SERVER_URL, json=payload, headers=HEADERS)
            print(f"\n--- Tool: {tool_name} ---")
            print(f"Status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"Error Body: {response.text}")
                return None
            
            result = response.json()
            return result
        except Exception as e:
            print(f"Request failed: {e}")
            return None

async def main():
    print("Fetching product list...")
    products_resp = await call_tool("list_products", {})
    print(f"Raw Response: {json.dumps(products_resp, indent=2)}")
    print("\nVerifying Customer...")
    auth_resp = await call_tool("verify_customer_pin", {
        "customer_id": "7912", 
        "pin": "7912"
    })
    
    if auth_resp:
        print("Auth check completed.")

if __name__ == "__main__":
    asyncio.run(main())