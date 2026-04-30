import os
import json
from google import generativeai as genai
from services.product_service import ProductService
from services.auth_service import AuthService

class MeridianChatbot:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.products = ProductService()
        self.auth = AuthService()
        
        # Define the tools available to the AI
        # We wrap your services so the LLM has a clean interface
        self.tools = [
            self.products.list_products,
            self.products.search_products,
            self.auth.get_customer,
            self.auth.verify_customer_pin
        ]
        
        self.model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            tools=self.tools,
            system_instruction=(
                "You are the Meridian Electronics Support Bot. "
                "1. Help users find products using search_products or list_products. "
                "2. For Order History or Placing Orders, you MUST first verify the customer "
                "using get_customer (to find their ID) and verify_customer_pin. "
                "3. Do not disclose order details unless verify_customer_pin returns success. "
                "4. Be concise, professional, and helpful."
            )
        )
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    async def handle_message(self, user_input: str):
        try:
            response = await self.chat.send_message_async(user_input)
            return response.text
        except Exception as e:
            return f"I'm sorry, I'm having trouble connecting to our systems: {str(e)}"