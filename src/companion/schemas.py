from pydantic import BaseModel, Field
from typing import Literal

class LessonRequest(BaseModel):
    topic: str=Field(min_length=2,max_length=120)
    mode: Literal["teach","quiz","review"] = "teach"

class LessonResult(BaseModel):
    explanation: str
    next_question:str | None = None
    confidence: float = Field(ge=0,le=1)
