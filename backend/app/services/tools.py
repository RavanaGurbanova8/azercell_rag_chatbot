# tools.py
import requests

def get_current_weather(location: str) -> str:
    try:
        r = requests.get(f"https://wttr.in/{location}?format=3", timeout=5)
        if r.ok:
            return r.text
    except Exception:
        pass
    return "Weather service unavailable"
