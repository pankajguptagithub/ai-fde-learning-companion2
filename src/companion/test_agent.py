from companion.agent import agent

def run_test(title: str,user_message: str)-> None:
    print(f"\n{'=' * 60}")
    print(title)
    print("=" *60)

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_message,
        }]
    })

    for message in result["messages"]:
        print(type(message).__name__,":",message.content)

run_test(
    "TEST 1: READ LEARNING PROFILE",
    (
        "Use the get_learning_profile tool to retrieve"
        "the profile for user123"
    ),
)

run_test(
    "TEST 2: SAVE VALID LEARNING ATTEMPT",
    (
        "Use the save_learning_attempt tool to save"
        "a score of 0.8 for topic RAg and user user123"
    ),
)

run_test(
    "TEST 3: REJECT INVALID SCORE",
    (
        "Use the save_learning_attempt tool to save"
        "a score of 1.5 for topic RAG and user user123"
    ),
)
