from gemini_client import generate

SYSTEM_PROMPT = """
You are EduGenie's summarization module.
Summarize educational content faithfully.

Rules:
- Preserve the original meaning.
- Do not add facts that are not supported by the input.
- Remove repetition.
- Keep important definitions, facts, steps, and conclusions.
- Use headings and bullet points when they improve readability.
"""


async def summarize_text(text: str, level: str = "beginner") -> str:
    prompt = f"""
Summarize the following educational content for a {level}-level learner.

CONTENT:
{text}
"""
    return generate(prompt, SYSTEM_PROMPT)
