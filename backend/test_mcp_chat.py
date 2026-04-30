import httpx
import asyncio

async def list_meridian_tools():
    url = "https://order-mcp-74afyau24q-uc.a.run.app/mcp"
    print(f"Directly querying {url} via POST with headers...")
    
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list", 
        "params": {}
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                tools = data.get("result", {}).get("tools", [])
                print(f"✅ Success! Found {len(tools)} tools.")
                for t in tools:
                    print(f" - {t['name']}")
                return tools
            else:
                print(f"❌ Server returned status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Direct request failed: {e}")
    
    return []
if __name__ == "__main__":
    asyncio.run(list_meridian_tools())