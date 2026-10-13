from typing import TypedDict, Literal

class LearningState(TypedDict, total=False):
	user_id: str
	topic: str
	mode: Literal["teach","quiz","review"]
	profile: dict
	evidence: list[dict]
	lesson: dict
	question: str
	learner_answer: str
	evaluation: dict
	attempts: int
	max_attempts: int
	next_action: Literal["teach", "retry", "advance","stop"]
	errors: list[str]

def should_continue(state: LearningState) -> str:
    if state.get("errors"):
        return "stop"
    if state.get("attempts",0) >= state.get("max_attempts",3):
        return "stop"
    if state.get("evaluation",{}).get("score",0)>= 0.8:
        return "advance"
    return "adapt"

state = {
    "attempts": 1,
    "max_attempts": 3,
    "evaluation":{
        "score":0.5
    }
}

print(should_continue(state))
