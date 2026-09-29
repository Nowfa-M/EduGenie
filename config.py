import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    app_name: str = os.getenv("APP_NAME", "EduGenie")
    max_output_tokens: int = int(os.getenv("MAX_OUTPUT_TOKENS", "2048"))
    temperature: float = float(os.getenv("TEMPERATURE", "0.3"))


settings = Settings()

if not settings.gemini_api_key:
    print("WARNING: GEMINI_API_KEY is not set. Add it to the .env file.")
