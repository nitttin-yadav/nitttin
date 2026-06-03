"""Pluggable AI conversation engine.

Supports "mock" (no external API) and "openai" providers.
Extend by adding new provider classes.
"""

import abc
import random

from app.config import settings


class AIProvider(abc.ABC):
    @abc.abstractmethod
    def generate_response(self, messages: list[dict], language: str = "en") -> str: ...


class MockProvider(AIProvider):
    RESPONSES_EN = [
        "I've noted that down. How can I help you further?",
        "Great question! Let me think about that for you.",
        "I'm here to help. Could you give me a bit more detail?",
        "That's an interesting thought. Let me help you organize it.",
        "I've updated your information. Anything else you'd like to do?",
        "I can help with that! Let me pull up the relevant details.",
        "Consider it done. What's next on your agenda?",
        "I'm on it. Let me work through this step by step.",
    ]
    RESPONSES_HI = [
        "मैंने यह नोट कर लिया है। मैं आपकी और कैसे मदद कर सकता हूं?",
        "बढ़िया सवाल! मुझे इस पर सोचने दीजिए।",
        "मैं यहाँ मदद के लिए हूँ। क्या आप थोड़ा और विस्तार से बता सकते हैं?",
        "यह एक दिलचस्प विचार है। मुझे इसे व्यवस्थित करने में मदद करने दें।",
        "मैंने आपकी जानकारी अपडेट कर दी है। और कुछ करना चाहेंगे?",
    ]

    def generate_response(self, messages: list[dict], language: str = "en") -> str:
        pool = self.RESPONSES_HI if language == "hi" else self.RESPONSES_EN
        return random.choice(pool)


class OpenAIProvider(AIProvider):
    def generate_response(self, messages: list[dict], language: str = "en") -> str:
        import httpx

        system_prompt = (
            "You are Ni, an AI Personal Operating System. "
            "You are helpful, warm, and intelligent. "
            f"Respond in {'Hindi' if language == 'hi' else 'English'}. "
            "Keep responses concise but helpful."
        )
        api_messages = [{"role": "system", "content": system_prompt}] + messages[-20:]

        resp = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {settings.OPENAI_API_KEY}"},
            json={"model": settings.OPENAI_MODEL, "messages": api_messages, "max_tokens": 1024},
            timeout=30.0,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]


_PROVIDERS: dict[str, type[AIProvider]] = {
    "mock": MockProvider,
    "openai": OpenAIProvider,
}


def get_ai_provider() -> AIProvider:
    cls = _PROVIDERS.get(settings.AI_PROVIDER, MockProvider)
    return cls()
