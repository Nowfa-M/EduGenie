from gemini_client import generate

SYSTEM_PROMPT = """
You are EduGenie's concept-explanation module.
Explain topics for students using simple language.

Structure:
- Meaning / definition
- Main idea
- Important points
- Simple example
- Short recap

Do not make up facts. If a topic has multiple accepted definitions,
mention the relevant context briefly.
"""


async def explain_topic(topic: str, level: str = "beginner") -> str:
    prompt = f"""
Explain this topic for a {level}-level learner:

{topic}

Use simple English and practical examples where useful.
"""
    return generate(prompt, SYSTEM_PROMPT)
