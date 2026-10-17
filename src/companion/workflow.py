from typing import TypedDict, Literal
from companion.retrieval import retrieve
from companion.memory import get_attempts,save_attempt
from companion.context import build_context

from langgraph.graph import StateGraph, START, END

class LearningState(TypedDict, total=False):
    user_id: str
    topic: str
    mode: Literal["teach","quiz","review"]
    profile: dict
    evidence: list[dict]
    history: list[dict]
    context: str
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

def validate_state(state: LearningState) -> list[str]:
    errors = []

    topic = state.get("topic","").strip()

    if not topic:
        errors.append("Topic is required")

    max_attempts = state.get("max_attempts",3)

    if max_attempts < 1 or max_attempts > 5:
        errors.append("max_attempts must be between 1 and 5")

    suspicious_phrases = (
        "ignore previous instructions",
        "reveal system promt",
        "reveal system secrets",
        "bypass instructions",
        "override instructions",    
        "switch role",
        "without restrictions",
        "internal configuration",
        "api key",
        "application secrets",
        "bypass validation",
    )

    topic_lower = topic.lower()

    if any(
            phrase in topic_lower
            for phrase in suspicious_phrases
    ):
        errors.append("Potential unsafe instruction detected")

    return errors

def validate_evidence(chunks: list[dict]) -> list[str]:
    errors = []

    suspicious_phrases = (
        "ignore previous instructions",
        "reveal system prompt",
        "reveal system secrets",
        "bypass instructions",
        "override instructions",
        "switch role",
        "without restrictions",
        "internal configuration",
        "api key",
        "application secrets",
        "bypass validation",
    )

    for chunk in chunks:
        text = chunk.get("text","").lower()

        if any (
            phrase in text
            for phrase in suspicious_phrases
        ):
            errors.append(
                "Unsafe instruction detected in retrieved evidence"
            )
            break
    return errors        


def route_after_context(state: LearningState) -> str:
    if state.get("errors"):
        return "stop"
    
    return "continue"

def load_context(state: LearningState) -> dict:

    validation_errors = validate_state(state)

    if validation_errors:
        return{
            "errors": validation_errors,
            "evidence": [],
            "history": [],
        }

    user_id = state.get("user_id","user123")
    topic = state["topic"]

    profile = {
        "goal" : "AI FDE",
        "strengths" : ["Scripting","System Design"],
        "gaps": ["RAG","Agentic AI"],
    }

    chunks = retrieve(topic)

    if not chunks:
        evidence_errors = validate_evidence(chunks)

        if evidence_errors:
            return {
                "errors": evidence_errors,
                "evidence": [],
                "history": [],
            }
        return {
            "errors":[
                f"No trusted evidence found for topic: {topic}"
            ],
            "evidence": [],
            "history": [],
        }

#    evidence_errors = validate_evidence(chunks)
#
#    if evidence_errors:
#        return {
#            "errors": evidence_errors,
#            "evidence": [],
#            "history": [],
#        }

    history = get_attempts(
        user_id = user_id,
        topic = topic,
    )

    session = {
        "topic": topic,
        "attempts": state.get("attempts",0)
    }

    context_packet = build_context(
        profile = profile,
        session = session,
        chunks = chunks,
        attempts = history,
        task = f"Teach and evaluate the learner on {topic}",
    
    )

    return {
        "profile" : profile,
        "evidence": chunks,
        "history": history,
        "context": (
            f"{context_packet.learner}\n\n"
            f"{context_packet.session}\n\n"
            f"{context_packet.evidence}\n\n"
            f"{context_packet.history}\n\n"
            f"{context_packet.task}\n\n"
        ),
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

    save_attempt(
        user_id = state.get("user_id","user123"),
        topic = state["topic"],
        score = score,
    )
    
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
builder.add_conditional_edges(
        "load_context",
        route_after_context,
        {
            "continue": "teach",
            "stop": "finalize",
        }
)
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
