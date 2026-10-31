import json
import requests
from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Any
from app.core.config import settings

router = APIRouter(prefix="/assistant", tags=["assistant"])

class AssistantRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    language: str = Field(default="en", pattern="^(en|hi|te)$")
    context: dict[str, Any] = Field(default_factory=dict)

class AssistantResponse(BaseModel):
    reply: str
    mode: str

GUIDANCE = {
    "en": "I can help explain mandi comparison, transport expenses and estimated net return. Load prices, enter realistic costs for each market, then compare. Sample values are not live prices. The estimate is not a guaranteed sale price or profit.",
    "hi": "मैं मंडी तुलना, परिवहन खर्च और अनुमानित शुद्ध कमाई समझाने में मदद कर सकता हूँ। भाव लोड करें, हर मंडी का वास्तविक खर्च भरें और तुलना करें। सैंपल आँकड़े लाइव भाव नहीं हैं। यह पक्की बिक्री कीमत या लाभ नहीं है।",
    "te": "మండి పోలిక, రవాణా ఖర్చులు మరియు అంచనా నికర ఆదాయాన్ని వివరించగలను. ధరలను తెచ్చి, ప్రతి మార్కెట్‌కు వాస్తవిక ఖర్చులు నమోదు చేసి పోల్చండి. నమూనా ధరలు ప్రత్యక్ష ధరలు కావు. ఇది హామీ ఇచ్చిన అమ్మకపు ధర లేదా లాభం కాదు."
}

@router.post("/chat", response_model=AssistantResponse)
def assistant_chat(payload: AssistantRequest):
    language = payload.language
    if settings.ai_api_key:
        base = settings.ai_base_url.rstrip("/")
        url = base if base.endswith("/chat/completions") else f"{base}/chat/completions"
        system = (
            "You are Mitra, a helpful agricultural market information guide for Indian farmers. "
            "Reply in the requested language (en=English, hi=Hindi, te=Telugu), using short, simple sentences. "
            "Use only the supplied context for any mandi prices or comparison results. Never invent prices, dates, distances, "
            "market availability, weather, or buyer demand. If the context lacks a fact, say it is unavailable and explain "
            "how to verify it. Do not guarantee profit or tell a farmer to travel/sell based on incomplete data. "
            "Explain that modal prices are indicative and actual sale prices vary by quality, grade, arrivals and buyers."
        )
        body = {"model": settings.ai_model, "temperature": 0.25, "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": f"Language: {language}\nContext: {json.dumps(payload.context, ensure_ascii=False)}\nQuestion: {payload.message}"}
        ]}
        try:
            response = requests.post(url, json=body, headers={"Authorization": f"Bearer {settings.ai_api_key}"}, timeout=20)
            response.raise_for_status()
            reply = response.json()["choices"][0]["message"]["content"].strip()
            if reply:
                return AssistantResponse(reply=reply, mode="configured_ai")
        except Exception:
            pass
    return AssistantResponse(reply=GUIDANCE[language], mode="guided_fallback")
