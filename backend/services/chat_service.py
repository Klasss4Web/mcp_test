import logging
import os
import asyncio
from google import generativeai as genai
from .product_service import ProductService
from .auth_service import AuthService
from core.errors import AppException
from openai import AsyncOpenAI
from dotenv import load_dotenv
from agents import Agent, Runner, trace, OpenAIChatCompletionsModel

load_dotenv(override=True)

groq_api_key = os.getenv('GROQ_API_KEY')
print(f"ChatService initialized with GROQ_API_KEY: {'set' if groq_api_key else 'not set'}")

class ChatService:
    def __init__(self):
        self.products = ProductService()
        self.auth = AuthService()
        self.chat_session = None

    async def initialize(self):
        # REMOVED: list_products_sync and other asyncio.run wrappers
        # These were causing the 500 error due to nested event loops.

        GROQ_BASE_URL = "https://api.groq.com/openai/v1"
        groq_client = AsyncOpenAI(base_url=GROQ_BASE_URL, api_key=groq_api_key)

        llama3_3_model = OpenAIChatCompletionsModel(
            model="llama-3.3-70b-versatile", 
            openai_client=groq_client
        )
        
        # Pass the ASYNC methods directly to mcp_servers. 
        # The 'agents' framework is designed to await these internally.
        agent = Agent(
            name="investigator", 
            instructions="""
                You are the Meridian Electronics Assistant. 
                Use search_products to find items. Use verify_customer_pin before
                discussing sensitive order details. Always be helpful and professional.
            """, 
            model=llama3_3_model,
            mcp_servers=[
                self.products.list_products,
                self.products.search_products,
                self.auth.get_customer,
                self.auth.verify_customer_pin
            ]
        )

        try:
            with trace("investigate"):
                # Runs your specific Banoffee task
                result = await Runner.run(agent, "Find a great recipe for Banoffee Pie, then summarize it in markdown to banoffee.md")
                print(result.final_output)
        except Exception as e:
            logging.error(f"Startup Investigation failed: {e}")
            # We don't necessarily want to crash the whole service if the recipe search fails

        # Initialize the persistent chat session
        self.genai_model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            tools=[
                self.products.list_products, 
                self.products.search_products, 
                self.auth.get_customer, 
                self.auth.verify_customer_pin
            ],
            system_instruction="You are the Meridian Electronics Assistant."
        )
        self.chat_session = self.genai_model.start_chat(enable_automatic_function_calling=True)

    async def chat(self, user_id: str, message: str):
        try:
            if not self.chat_session:
                await self.initialize()
            
            response = await self.chat_session.send_message_async(message)
            return {"response": response.text}
            
        except Exception as e:
            logging.error(f"Agent Logic Error: {str(e)}")
            # This is where your 500 comes from if anything above fails
            raise AppException(f"Agent Logic Error: {str(e)}")