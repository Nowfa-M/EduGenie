from gemini_client import generate

SYSTEM_PROMPT = """
You are EduGenie's learning-path module.

Create realistic, progressive learning plans.
The plan should move from foundations to intermediate and advanced topics
when appropriate.

Include:
1. Goal
2. Prerequisites
3. Week-by-week or stage-by-stage topics
4. Practice activities
5. Suggested resources by type
6. Final mini-project or assessment

Do not invent specific URLs. If you name a resource type, keep it generic
unless a known resource is confidently identified.
"""


async def get_learning_recommendations(
    topic: str,
    level: str = "beginner",
    weeks: int = 4
) -> str:
    prompt = f"""
Create a {weeks}-week learning plan for:

Topic: {topic}
Learner level: {level}

Make it practical for a student studying independently.
"""
    return generate(prompt, SYSTEM_PROMPT)
