import json
from typing import List
from pydantic import BaseModel, Field
from gemini_client import generate


class QuizQuestion(BaseModel):
    question: str
    options: List[str] = Field(min_length=4, max_length=4)
    answer: str
    explanation: str


class QuizResponse(BaseModel):
    topic: str
    questions: List[QuizQuestion]


QUIZ_SCHEMA = {
    "type": "object",
    "properties": {
        "topic": {"type": "string"},
        "questions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                    "options": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 4,
                        "maxItems": 4
                    },
                    "answer": {"type": "string"},
                    "explanation": {"type": "string"}
                },
                "required": ["question", "options", "answer", "explanation"]
            }
        }
    },
    "required": ["topic", "questions"]
}


async def generate_quiz(
    topic: str,
    level: str = "beginner",
    count: int = 5
) -> QuizResponse:
    system = """
You are EduGenie's quiz generator.

Create educational multiple-choice questions.
Every question must have exactly four options and exactly one correct answer.

Rules:
- Questions must match the requested topic and learner level.
- The correct answer must be one of the four options.
- Do not create trick questions unless explicitly requested.
- Explanations must briefly explain why the answer is correct.
- Never invent technical facts.
"""

    prompt = f"""
Topic: {topic}
Learner level: {level}
Number of questions: {count}

Return JSON only matching this schema:
{json.dumps(QUIZ_SCHEMA, indent=2)}
"""

    raw = generate(prompt, system, response_schema=QUIZ_SCHEMA)
    data = json.loads(raw)

    if len(data.get("questions", [])) != count:
        raise ValueError(
            f"Gemini returned {len(data.get('questions', []))} questions; expected {count}."
        )

    for item in data["questions"]:
        if len(item["options"]) != 4:
            raise ValueError("Each quiz question must contain exactly 4 options.")
        if item["answer"] not in item["options"]:
            raise ValueError("A quiz answer was not present in its options.")

    return QuizResponse.model_validate(data)
