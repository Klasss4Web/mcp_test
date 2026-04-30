import logging
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool 
from .product_service import ProductService
from .auth_service import AuthService
from core.errors import AppException

load_dotenv(override=True)

class ChatService:
    def __init__(self):
        self.products = ProductService()
        self.auth = AuthService()
        self.agent = None
        self.initialized = False
        self.groq_api_key = os.getenv('GROQ_API_KEY')

    async def initialize(self):
        if self.initialized: return

        if not self.groq_api_key:
            raise AppException("GROQ_API_KEY is missing.")

        groq_client = AsyncOpenAI(
            base_url="https://api.groq.com/openai/v1", 
            api_key=self.groq_api_key
        )

        llama_model = OpenAIChatCompletionsModel(
            model="llama-3.3-70b-versatile", 
            openai_client=groq_client
        )
        
        # Create tools
        list_tool = function_tool(self.products.list_products)
        search_tool = function_tool(self.products.search_products)
        verify_tool = function_tool(self.auth.verify_customer_pin)
        customer_tool = function_tool(self.auth.get_customer)

        for tool in [list_tool, search_tool, verify_tool, customer_tool]:
            if hasattr(tool, 'definition') and isinstance(tool.definition, dict):
                fn = tool.definition.get("function", {})
                params = fn.get("parameters", {})
                
                # Ensure the root parameters type is 'object'
                if "type" not in params:
                    params["type"] = "object"
                
                # Ensure 'properties' exists as a dictionary
                if "properties" not in params or not params["properties"]:
                    params["properties"] = {}
                    
                # Groq strictly requires 'properties' if 'type' is 'object'
                fn["parameters"] = params

        self.agent = Agent(
            name="MeridianAssistant", 
            instructions="You are a helpful electronics store assistant.", 
            model=llama_model,
            tools=[list_tool, search_tool, verify_tool, customer_tool]
        )
        self.initialized = True

    async def chat(self, user_id: str, message: str):
        try:
            if not self.initialized: await self.initialize()
            result = await Runner.run(self.agent, message)
            return {"response": result.final_output}
        except Exception as e:
            logging.error(f"Chat Logic Error: {str(e)}")
            # Catching the specific Groq schema error message
            if "failed to validate" in str(e).lower() or "400" in str(e):
                return {"response": "I'm having trouble connecting to my tools. Please try again in a moment."}
            raise AppException(f"Assistant Error: {str(e)}")