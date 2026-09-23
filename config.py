import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "django" / "docs"
CHROMA_DB_DIR = BASE_DIR / "chroma_db"

TARGET_FOLDERS = []

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

PRIMARY_MODEL = "groq/openai/gpt-oss-120b"
FALLBACK_MODELS = [
    "groq/qwen/qwen3.6-27b",
    "gemini/gemini-3.6-flash",
    "gemini/gemini-3.5-flash-lite",
]

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")