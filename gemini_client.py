from google import genai
from google.genai import types

from config import settings


def get_client() -> genai.Client:
    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Create a .env file and add your Gemini API key."
        )
    return genai.Client(api_key=settings.gemini_api_key)


def generate(
    prompt: str,
    system_instruction: str,
    use_web: bool = False,
    response_schema=None,
):
    client = get_client()

    tools = None
    if use_web:
        tools = [
            types.Tool(
                google_search=types.GoogleSearch()
            )
        ]

    config_kwargs = {
        "system_instruction": system_instruction,
        "temperature": settings.temperature,
        "max_output_tokens": settings.max_output_tokens,
    }

    if tools:
        config_kwargs["tools"] = tools

    if response_schema is not None:
        config_kwargs["response_mime_type"] = "application/json"
        config_kwargs["response_schema"] = response_schema

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=types.GenerateContentConfig(**config_kwargs),
    )

    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text
