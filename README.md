# Meridian Electronics Customer Support Chatbot

## Overview
A full-stack AI-powered customer support chatbot for Meridian Electronics, featuring:
- FastAPI backend (Python)
- Vite + React frontend
- MCP server integration for product/order/customer tools
- Modern, floating chat widget UI

## Features
- Product availability lookup
- Order placement
- Order history
- Customer authentication
- AI chat assistant (Gemini/LLM)

## Project Structure
- `backend/` — FastAPI app, MCP integration, services, routers
- `frontend/` — Vite + React SPA, chat widget, modern CSS
- `terraform/` — Infrastructure as code
- `sample/` — Example deployments

## How to Run the App

### 1. Backend (FastAPI)
- Navigate to the backend folder:
  ```bash
  cd backend
  ```
- Install dependencies (recommended: use a virtual environment):
  ```bash
  pip install -r requirements.txt
  ```
- Copy and configure your `.env` file with the required API keys and settings.
- Start the FastAPI server:
  ```bash
  uvicorn main:app --reload
  ```
- The backend will be available at `http://localhost:8000`

### 2. Frontend (Vite + React)
- Navigate to the frontend folder:
  ```bash
  cd frontend
  ```
- Install dependencies:
  ```bash
  npm install
  ```
- Start the development server:
  ```bash
  npm run dev
  ```
- The frontend will be available at `http://localhost:5173`

### 3. Access the App
- Open your browser and go to `http://localhost:5173`
- The frontend will communicate with the backend via the `/api` proxy.

## Deployment
- **Backend:** Render.com (use `uvicorn main:app --host 0.0.0.0 --port $PORT`)
- **Frontend:** Vercel.com (auto-detects Vite)
- **CORS:** Configured for both local and cloud domains

## Environment Variables
See `backend/.env` for API keys and config.

## Architectural Decisions
See `architectural_decision.md` for rationale and key choices.

---
_Last updated: 2026-04-30_
