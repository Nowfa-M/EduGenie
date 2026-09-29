from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import Literal

from config import settings
from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

app = FastAPI(
    title="EduGenie - Google Gemini Powered Learning Assistant",
    version="1.0.0",
    description="AI learning assistant powered by Google Gemini."
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)
    level: str = Field(default="beginner", max_length=30)


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=10000)
    level: str = Field(default="beginner", max_length=30)
    use_web: bool = False


class QuizRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=300)
    level: str = Field(default="beginner", max_length=30)
    count: int = Field(default=5, ge=3, le=10)


class LearningPathRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=300)
    level: str = Field(default="beginner", max_length=30)
    weeks: int = Field(default=4, ge=1, le=12)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
   return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={}
)


@app.get("/health")
async def health():
    return {"status": "ok", "model": settings.gemini_model}


@app.post("/api/qa")
async def qa(payload: QuestionRequest):
    try:
        result = await answer_question(
            payload.question,
            payload.level,
            payload.use_web
        )
        return {"success": True, "result": result}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/api/explain")
async def explain(payload: TextRequest):
    try:
        result = await explain_topic(payload.text, payload.level)
        return {"success": True, "result": result}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/api/quiz")
async def quiz(payload: QuizRequest):
    try:
        result = await generate_quiz(payload.topic, payload.level, payload.count)
        return {"success": True, "result": result.model_dump()}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/api/summarize")
async def summarize(payload: TextRequest):
    try:
        result = await summarize_text(payload.text, payload.level)
        return {"success": True, "result": result}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/api/learn/recommendations")
async def recommendations(payload: LearningPathRequest):
    try:
        result = await get_learning_recommendations(
            payload.topic,
            payload.level,
            payload.weeks
        )
        return {"success": True, "result": result}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
