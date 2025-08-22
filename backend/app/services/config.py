import os


AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
BEDROCK_MODEL_ID = os.getenv(
"BEDROCK_MODEL_ID",
"us.anthropic.claude-3-7-sonnet-20250219-v1:0",
)


KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID")
KB_TOP_K = int(os.getenv("KB_TOP_K", "3"))


BACKEND_HOST = os.getenv("BACKEND_HOST", "0.0.0.0")
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))