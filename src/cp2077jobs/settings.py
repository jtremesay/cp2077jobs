from os import environ
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path()

HTML_DIR = BASE_DIR / "html"

if (OLLAMA_BASE_URL := environ.get("OLLAMA_BASE_URL")) is None:
    OLLAMA_BASE_URL = "http://localhost:11434/v1"
    environ["OLLAMA_BASE_URL"] = OLLAMA_BASE_URL

MODEL_NAME = "bedrock:eu.anthropic.claude-haiku-4-5-20251001-v1:0"
# MODEL_NAME = "bedrock:eu.anthropic.claude-sonnet-4-20250514-v1:0"
# MODEL_NAME = "bedrock:eu.anthropic.claude-sonnet-4-5-20250929-v1:0"
# MODEL_NAME = "bedrock:eu.anthropic.claude-sonnet-4-6"
# MODEL_NAME = "ollama:ministral-3:3b"
