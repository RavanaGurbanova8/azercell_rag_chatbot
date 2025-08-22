from typing import List, Dict, Optional


Message = Dict[str, str]


def add_user_message(messages: List[Message], content: str) -> List[Message]:
    messages.append({"role": "user", "content": content})
    return messages


def add_assistant_message(messages: List[Message], content: str) -> List[Message]:
    messages.append({"role": "assistant", "content": content})
    return messages