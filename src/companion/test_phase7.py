from companion.workflow import graph
from companion.memory import get_attempts

USER_ID = "phase7_user"
TOPIC = "RAG"

# Memory before workflow execution

before = get_attempts(
    user_id = USER_ID,
    topic = TOPIC,
)

print("Attempts before:", len(before))


#Executing full LangGraph workflow
result = graph.invoke(
    {
        "user_id": USER_ID,
        "topic": TOPIC,
        "mode": "quiz",
        "learner_answers": [
            "RAG uses a knowledge base",
            (
                "RAG combines retrieval of external information"
                "with generation by an LLM"
            ),
        ],
        "attempts": 0,
        "max_attempts": 3,
        "errors": [],
    }
)

# Memory after workflow execution
after = get_attempts(
    user_id = USER_ID,
    topic = TOPIC,
)

print("\n === RAG ===")
print("Retrieved sources:")

for document in result["evidence"]:
    print(document["source"])

print("\n=== WORKFLOW ===")
print("Total attempts:",result["attempts"])
print("Final score:", result["evaluation"]["score"])
print("Next action:",result["next_action"])


print("\n === MEMORY ===")
print("Attempts after:",len(after))
print("New attempts saved:", len(after) - len(before))


for attempt in after:
    print(
        attempt["topic"],
        attempt["score"],
    )

print("\n=== CONTEXT ===")
print(result["context"])
