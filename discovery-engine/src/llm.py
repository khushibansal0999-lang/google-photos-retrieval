"""Thin Gemini wrapper (free tier). One place to change model / provider.

Env: GEMINI_API_KEY (from aistudio.google.com — free, no card).
"""
import json, os, time, warnings
from pathlib import Path
from dotenv import load_dotenv

warnings.filterwarnings("ignore")
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

from google import genai
from google.genai import types

# Free-tier quotas differ per model; we walk this list on 429s.
MODELS = [m for m in os.environ.get("GEMINI_MODELS", "gemini-3.5-flash-lite,gemini-3.1-flash-lite,gemini-3-flash-preview,gemini-3.6-flash").split(",") if m]
MODEL = MODELS[0]
_client = None

def client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    return _client


def _is_quota(msg: str) -> bool:
    return any(k in msg for k in ("429", "RESOURCE_EXHAUSTED", "503", "500", "overloaded", "UNAVAILABLE"))


def generate_json(system: str, user: str, schema: dict, max_retries: int = 3, temperature: float = 0.1):
    """Return parsed JSON matching `schema`. On quota errors, retries briefly then falls to the next model."""
    last = None
    for model in MODELS:
        delay = 8
        for attempt in range(max_retries):
            try:
                resp = client().models.generate_content(
                    model=model, contents=user,
                    config=types.GenerateContentConfig(
                        system_instruction=system, response_mime_type="application/json",
                        response_json_schema=schema, temperature=temperature,
                    ),
                )
                return json.loads(resp.text)
            except Exception as e:
                last = e
                if not _is_quota(str(e)): raise
                if attempt < max_retries - 1: time.sleep(delay); delay *= 2
        print(f"  [llm] {model} exhausted, falling back", flush=True)
    raise last


def generate_text_stream(system: str, user: str, temperature: float = 0.3):
    for chunk in client().models.generate_content_stream(
        model=MODELS[0], contents=user,
        config=types.GenerateContentConfig(system_instruction=system, temperature=temperature),
    ):
        if chunk.text:
            yield chunk.text
