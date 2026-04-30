


import logging
import os
from google import generativeai as genai
from .product_service import ProductService
from .auth_service import AuthService
from core.errors import AppException

class ChatService:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        
        self.products = ProductService()
        self.auth = AuthService()

        self.model = genai.GenerativeModel(
            model_name='gemini-3-flash-preview',
            tools=[
                self.products.list_products,
                self.products.search_products,
                self.auth.get_customer,
                self.auth.verify_customer_pin
            ],
            system_instruction=(
                "You are the Meridian Electronics Assistant. "
                "Use search_products to find items. Use verify_customer_pin before "
                "discussing sensitive order details. Always be helpful and professional."
            )
        )
        self.chat_session = self.model.start_chat(enable_automatic_function_calling=True)

    async def chat(self, user_id: str, message: str):
        try:
            response = await self.chat_session.send_message_async(message)
            
            return {"response": response.text}
            
        except Exception as e:
            logging.error(f"Agent Logic Error: {str(e)}")
            raise AppException("I'm having trouble thinking right now. Please try again.")