from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END

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

    if state.get("evaluation",{}).get("score",0) >= 0.8:
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

def load_context(state):
    return state

def teach(state):
    return state

def ask_question(state):
    return state

def adapt_lesson(state):
    return state

def finalize_session(state):
    return state

def evaluate_answer(state: LearningState) -> dict:
    prompt = build_evaluation_prompt(
        topic = state["topic"],
        question = state["question"],
        answer = state["learner_answer"],
        evidence = state.get("evidence",[]),
    )
    evaluation = evaluator_model.with_structured_output(
        AnswerEvaluation
    ).invoke(prompt)
    return {
        "evaluation": evaluation.model_dump(),
        "attempts": state.get("attempts",0)+1,
    }

def approval_required(state: LearningState) -> str:
    proposed = state.get("proposed_profile_update")
    return "approve" if proposed else "continue"

builder = StateGraph(LearningState)
builder.add_node("load_context",load_context)
builder.add_node("teach",teach)
builder.add_node("ask",ask_question)
builder.add_node("evaluate",evaluate_answer)
builder.add_node("adapt",adapt_lesson)
builder.add_node("finalize",finalize_session)

builder.add_edge(START,"load_context")
builder.add_edge("load_context","teach")
builder.add_edge("teach","ask")
builder.add_edge("ask","evaluate")
builder.add_conditional_edges(
        "evaluate",
        should_continue,
        {"adapt": "adapt", "advance":"finalize", "stop": "finalize"},
        )
builder.add_edge("adapt","ask")
builder.add_edge("finalize",END)
graph = builder.compile()
