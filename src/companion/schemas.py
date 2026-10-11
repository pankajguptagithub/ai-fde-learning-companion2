from pydantic import BaseModel, Field
from typing import Literal

class LessonRequest(BaseModel):
    topic: str=Field(min_length=2,max_length=120)
    mode: Literal["teach","quiz","review"] = "teach"

class LessonResult(BaseModel):
    explanation: str
    next_question:str | None = None
    confidence: float = Field(ge=0,le=1)

class TutorTurn(BaseModel):
    concept: str
    explanation: str
    example: str
    diagnostic_question: str
    prerequisites_missing: list[str] = []
    confidence: float = Field(ge=0, le=1)


client = OpenAI()
response = client.responses.parse(
    model = settings.openai_model,
    instructions = TUTOR_SYSTEM,
    input = "Teach reranking to a learner who understands vector search",
    text_format = TutorTurn,
)
turn = response.output_parsed
