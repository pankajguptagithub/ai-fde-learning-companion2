from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from companion.model import safe_ask
from companion.workflow import graph

app = FastAPI(
    title = "AI FDE Learning Companion",
    version = "1.0.0",
)

class LearnRequest(BaseModel):
    user_id: str = Field(min_length=1)
    topic: str = Field(min_length=1,max_length=120)
    #mode: str = "quiz"
    mode: Literal["teach","quiz","review"] = "quiz"
    learner_answers: list[str] = []
    max_attempts: int = Field(default=3, ge=1, le=5)

class ChatRequest(BaseModel):
    question: str = Field(min_length=1)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(request: ChatRequest):
    answer = safe_ask(request.question)

    return{
        "question": request.question,
        "answer": answer,
    }

@app.post("/learn")
def learn(request: LearnRequest):
    try:
        result = graph.invoke(
            {
                "user_id": request.user_id,
                "topic": request.topic,
                "mode": request.mode,
                "learner_answers": request.learner_answers,
                "attempts": 0,
                "max_attempts": request.max_attempts,
                "errors": [],
            }
        )

        return result

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            details=str(exc),
        )from exc

    except Exception as exc:
        raise HTTPException(
            status_code = 503,
            detail = "Learning service unavailable",
        )from exc
