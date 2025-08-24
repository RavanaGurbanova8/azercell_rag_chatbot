# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import boto3
from app.routes.chat import router as chat_router

# -------------------------------
# Load environment variables
# -------------------------------
load_dotenv()  # loads .env file

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")  # default fallback

if not AWS_ACCESS_KEY or not AWS_SECRET_KEY:
    raise ValueError("AWS credentials not found in .env file!")

# -------------------------------
# Initialize Boto3 client for Bedrock
# -------------------------------
runtime = boto3.client(
    "bedrock-runtime",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# -------------------------------
# FastAPI app setup
# -------------------------------
app = FastAPI(title="RAG Chatbot Backend", version="0.1.0")

# CORS middleware (frontend ↔ backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router)

# -------------------------------
# Health check endpoint
# -------------------------------
@app.get("/health")
async def health():
    return {"status": "ok"}

# -------------------------------
# Chat endpoint
# -------------------------------
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    # Example: Replace this with actual Bedrock call
    # response = runtime.invoke_model(...)

    return {"reply": f"You said: {request.message}"}
