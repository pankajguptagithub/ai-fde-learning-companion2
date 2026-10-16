from companion.memory import save_attempt, get_attempts

save_attempt(
    user_id="user123",
    topic="RAG",
    score=0.5,
)

save_attempt(
    user_id="user123",
    topic="RAG",
    score=0.9,
)

attempts = get_attempts(
    user_id="user123",
    topic="RAG",
)

print("Saved attempts")

for attempt in attempts:
    print(
        attempt["topic"],
        attempt["score"],
    )
