from fastapi import FastAPI
from core.config import get_settings
from core.logging import setup_logging
from core.errors import app_exception_handler, validation_exception_handler, AppException
from fastapi.exceptions import RequestValidationError
from api import chat, auth, orders, products

settings = get_settings()
setup_logging(settings.LOG_LEVEL)

app = FastAPI(title="Meridian Customer Support Chatbot")

# Register routers
api_prefix = "/api"
app.include_router(chat.router, prefix=api_prefix)
app.include_router(auth.router, prefix=api_prefix)
app.include_router(orders.router, prefix=api_prefix)
app.include_router(products.router, prefix=api_prefix)

# Register error handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/healthz")
def health_check():
    return {"status": "ok"}
