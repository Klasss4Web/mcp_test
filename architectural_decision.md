# Architectural Decision Record

## Overview
This document captures key architectural decisions for the Meridian Electronics Customer Support Chatbot project.

## 1. Technology Stack
- **Backend:** FastAPI (Python), async MCP integration, Pydantic for config and validation
- **Frontend:** Vite + React, modern CSS, floating chat widget
- **MCP Server:** JSON-RPC API for product, order, and customer tools
- **Deployment:** Render (backend), Vercel (frontend)

## 2. API Design
- RESTful endpoints for products, orders, authentication, and chat
- Chat endpoint integrates with Gemini/LLM and MCP tools

## 3. Security
- CORS configured for frontend/backend domains
- Sensitive endpoints require authentication

## 4. Error Handling
- Robust error handling in backend and frontend
- User-friendly error messages in UI

## 5. Extensibility
- Modular backend services and routers
- Frontend component-based architecture

## 6. Rationale
- FastAPI chosen for async support and rapid development
- Vite/React for modern SPA experience
- MCP for tool orchestration and extensibility

---
Document updated: 2026-04-30
