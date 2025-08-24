# backend/app/services/kb_runtime.py
import boto3
from app.services.config import AWS_REGION, KNOWLEDGE_BASE_ID, KB_TOP_K, AWS_ACCESS_KEY, AWS_SECRET_KEY

agent = boto3.client(
    "bedrock-agent-runtime",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

def get_kb_context(user_query: str) -> str:
    if not KNOWLEDGE_BASE_ID:
        return ""
    try:
        req = {
            "knowledgeBaseId": KNOWLEDGE_BASE_ID,
            "retrievalQuery": {"text": user_query},
            "retrievalConfiguration": {
                "vectorSearchConfiguration": {"numberOfResults": KB_TOP_K}
            },
        }
        resp = agent.retrieve(**req)
        cands = resp.get("retrievalResults", [])
        parts = [f"Doc {i+1}: {c.get('content', {}).get('text', '')}" for i, c in enumerate(cands) if c.get('content', {}).get('text')]
        return "\n\n".join(parts)
    except Exception:
        return ""
