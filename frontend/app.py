import os
import requests
import streamlit as st


BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


st.set_page_config(page_title="RAG Chatbot", layout="wide")
st.title("RAG Chatbot (Bedrock)")


# Controls
use_kb = st.toggle("Use Knowledge Base", value=True)
stream = st.toggle("Stream response", value=True)
col1, col2 = st.columns([3, 1])
with col2:
    temperature = st.slider("Temperature", 0.0, 1.0, 0.5, 0.1)
    max_tokens = st.number_input("Max tokens", min_value=128, max_value=4096, value=1024, step=64)


prompt = st.text_area("You:", height=120)


if st.button("Send", use_container_width=True) and prompt.strip():
    payload = {
        "prompt": prompt,
        "use_kb": use_kb,
        "stream": stream,
        "temperature": float(temperature),
        "max_tokens": int(max_tokens),
    }

if stream:
    st.write("**Assistant:**")
    placeholder = st.empty()
    text = ""
    with st.spinner("Thinking..."):
        r = requests.post(f"{BACKEND_URL}/chat/stream", json=payload, stream=True)
        r.raise_for_status()
        for chunk in r.iter_content(decode_unicode=True):
            if chunk:
                text += chunk
                placeholder.write(text)
else:
    with st.spinner("Thinking..."):
        r = requests.post(f"{BACKEND_URL}/chat", json=payload)
        r.raise_for_status()
        data = r.json()
        st.write("**Assistant:**")
        st.write(data.get("answer", ""))