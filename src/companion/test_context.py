from companion.context import build_context
from companion.retrieval import retrieve
from companion.memory import get_attempts

profile = {
    "goal" : "AI FDE",
    "strengths" : ["Golang","System Design"],
    "gaps": ["RAG"],
}

session = {
    "topic": "RAG",
    "attempts": 0,
}

chunks = retrieve("What is reranking in RAG?")

attempts = get_attempts(
    user_id = "user123",
    topic = "RAG",
)

context = build_context(
        profile=profile,
        session=session,
        chunks=chunks,
        attempts=attempts,
        task="Explain reranking in RAG",
        )

print("=== LEARNER ===")
print(context.learner)

print("\n === SESSION ===")
print(context.session)

print("\n === EVIDENCE ===")
print(context.evidence)

print("\n === HISTORY ===")
print(context.history)

print("\n === TASK ===")
print(context.task)
