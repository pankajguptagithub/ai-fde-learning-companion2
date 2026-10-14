from typing import TypedDict, Literal

from langgraph.graph import StateGraph, START, END

class LearningState(TypedDict, total=False):
    user_id: str
    topic: str
    mode: Literal["teach","quiz","review"]
    profile: dict
    evidence: list[dict]
    lesson: str
    question: str
    learner_answers: list[str]
    current_answer: str
    evaluation: dict
    attempts: int
    max_attempts: int
    next_action: Literal["adapt","advance","stop"]
    final_message: str
    errors: list[str]

def load_context(state: LearningState) -> dict:
    return {
        "profile":{
            "goal" : "AI FDE",
            "strengths" : ["Scripting","System Design"],
            "gaps": ["RAG","Agentic AI"],
        },
        "evidence":[
            {
                "id": "rag-001",
                "text": (
                    "RAG combines retrieval from an external"
                    "knowledge source with model generation"
                ),
            }
        ],
    } 


def teach(state: LearningState) -> dict:
    return{
        "lesson":(
            "RAG works in two stages retrieves relevant external information"
            "and provides it to the model before generation"
        )
    }

def ask_question(state: LearningState) -> dict:
    attempt_number = state.get("attempts",0)+1

    return {
        "question":(
            f"Attempt {attempt_number}:"
            "What are the two main components involved in RAG?"
        )
    }

def evaluate_answer(state: LearningState) -> dict:
    attempts = state.get("attempts",0)
    answers = state.get("learner_answers",[])

    if attempts < len(answers):
        answer = answers[attempts]
    else:
        answer = ""

    answer_lower = answer.lower()
    
    #print("Answers =",answers)
    #print("Attempts=",attempts)
    #print("Chosen Answer=",answer)

    mentions_retrieval = (
        "retrieval" in answer_lower
        or "retrieve" in answer_lower
        or "knowledge base" in answer_lower
        or "external knowledge" in answer_lower
    )

    mentions_generation = (
        "generation" in answer_lower
        or "generate" in answer_lower
        or "model" in answer_lower
        or "llm" in answer_lower
    )

    if mentions_retrieval and mentions_generation:
        score = 0.9
        feedback = "Correct: RAG combines retrieval and generation"
    elif mentions_retrieval or mentions_generation:
        score = 0.5
        feedback = "Partially correct. Mention both retrieval and generation"
    else:
        score = 0.2
        feedback = "Incorrect. Review retrieval and generation"
    
    return {
        "current_answer" : answer,
        "evaluation" : {
            "score": score,
            "feedback": feedback,
        },
        "attempts": attempts + 1,
    }

def should_continue(state: LearningState) -> str:
    if state.get("errors"):
        return "stop"

    score = state.get("evaluation", {}).get("score",0)

    if score >= 0.8:
        return "advance"

    if state.get("attempts",0) >= state.get("max_attempts",3):
        return "stop"


    return "adapt"

def adapt_lesson(state: LearningState) -> dict:
    return {
        "next_action": "adapt",
        "lesson": (
            "Think of RAG as two steps: first retrieve relevant"
            "information, then let the model generate an answer"
        ),
    }

def finalize_session(state: LearningState) -> dict:
    score = state.get("evaluation",{}).get("score",0)

    if state.get("errors"):
        message = "Session stopped because an error occured"
        action = "stop"
    elif score >= 0.8:
        message = "Concept understood.You can advance"
        action = "advance"
    else:
        message = "Maximum attempts reached. Review the concept again"
        action = "stop"
     
    return {
        "next_action": action,
        "final_message": message,
    }

def approval_required(state: LearningState) -> str:
    proposed_update = state.get("proposed_profile_update")
    return "approve" if proposed_update else "continue"

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
        {
            "adapt": "adapt", 
            "advance":"finalize", 
            "stop": "finalize"
        },
)
builder.add_edge("adapt","ask")
builder.add_edge("finalize",END)
graph = builder.compile()
