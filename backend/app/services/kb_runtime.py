from typing import Optional
import boto3
from app.services.config import AWS_REGION, KNOWLEDGE_BASE_ID, KB_TOP_K


# Bedrock Agent Runtime (Knowledge Bases)
agent = boto3.client("bedrock-agent-runtime", region_name=AWS_REGION)




def get_kb_context(user_query: str) -> str:
	"""Return a small concatenated context string from Bedrock Knowledge Base.
	If KNOWLEDGE_BASE_ID is not set, return empty string.
	"""
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
		parts = []
		for i, c in enumerate(cands):
			content = c.get("content", {}).get("text", "")
			if content:
				parts.append(f"Doc {i+1}: {content}")
		return "\n\n".join(parts)
	except Exception as e:
		# In production, log this
		return ""