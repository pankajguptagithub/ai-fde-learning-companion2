from companion.workflow import graph

def run_scenario(
        title: str, 
        learner_answers: list[str]
) -> None:
 
    print(f"\n{'=' * 60}")
    print(title)
    print("=" * 60)

    result = graph.invoke(
        {
            "user_id": "user123",
            "topic": "RAG",
            "mode": "quiz",
            "learner_answers": learner_answers,           
            "attempts": 0,
            "max_attempts": 3,
            "errors": [],
        }
    )

    print("Final lesson:", result["lesson"])
    print("Final question:", result["question"])
    print("Final answer:", result["learner_answers"])
    print("Total attempts:",result["attempts"])
    print("Evaluation:",result["evaluation"])
    print("Next action:",result["next_action"])
    print("Final message:",result["final_message"])

run_scenario(
    "SCENARIO 1: CORRECT ON FIRST ATTEMPT",
    [
        (
        "RAG combines retreival from an external knowledge base"
        "with generation by an LLM"
        )
    ],
)
run_scenario(
    "SCENARIO 2: RETRY THEN CORRECT",
    [
        "RAG uses a knowledge base",
        (
            "RAG combines retrieval of external information"
            "with generation by a model"
        ),
    ],
)
run_scenario(
    "SCENARIO 3: MAXIMUM ATTEMPTS REACHED",
    [
        "RAG is a database",
        "RAG stores documents",
        "RAG is an AI application"
    ],
)
