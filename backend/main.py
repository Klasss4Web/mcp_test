
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import get_settings
from core.logging import setup_logging
from core.errors import app_exception_handler, validation_exception_handler, AppException
from fastapi.exceptions import RequestValidationError
from api import chat, auth, orders, products


settings = get_settings()
setup_logging(settings.LOG_LEVEL)


app = FastAPI(title="Meridian Customer Support Chatbot")

# CORS setup
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://mcp-test-sooty.vercel.app",
    "https://mcp-test-fyem.onrender.com",
]
if hasattr(settings, "CORS_ORIGINS") and settings.CORS_ORIGINS:
    origins += [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

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
