# backend/app/services/bedrock_runtime.py
import json
import boto3
from typing import Iterable, List, Dict, Optional
from app.services.config import AWS_REGION, BEDROCK_MODEL_ID, AWS_ACCESS_KEY, AWS_SECRET_KEY

runtime = boto3.client(
    "bedrock-runtime",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

AnthropicBody = Dict[str, object]

def _build_body(messages: List[Dict[str, str]], system: Optional[str], temperature: float, max_tokens: int) -> AnthropicBody:
    body: AnthropicBody = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": messages,
    }
    if system:
        body["system"] = system
    return body

def invoke_non_stream(messages: List[Dict[str, str]], system: Optional[str] = None, temperature: float = 0.5, max_tokens: int = 1024) -> str:
    try:
        body = _build_body(messages, system, temperature, max_tokens)
        resp = runtime.invoke_model(modelId=BEDROCK_MODEL_ID, body=json.dumps(body))
        payload = json.loads(resp["body"].read().decode("utf-8"))
        blocks = payload.get("content", [])
        if blocks and isinstance(blocks, list):
            first = blocks[0]
            if isinstance(first, dict):
                return first.get("text", "")
        return ""
    except Exception as e:
        return f"Error invoking model: {str(e)}"

def stream_deltas(messages: List[Dict[str, str]], system: Optional[str] = None, temperature: float = 0.5, max_tokens: int = 1024) -> Iterable[str]:
    body = _build_body(messages, system, temperature, max_tokens)
    try:
        stream = runtime.invoke_model_with_response_stream(
            modelId=BEDROCK_MODEL_ID,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(body),
        )
        for event in stream.get("body", []):
            chunk = event.get("chunk")
            if not chunk:
                continue
            try:
                decoded = json.loads(chunk.get("bytes").decode("utf-8"))
            except Exception:
                continue
            delta = decoded.get("delta", {})
            text = delta.get("text", "")
            if text:
                yield text
    except Exception as e:
        yield f"Error streaming model: {str(e)}"
