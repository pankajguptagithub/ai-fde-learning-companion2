from companion.model import ask_model, evaluate_answer
from companion.workflow import should_continue

if __name__ == "__main__":
    topic = input("Topic: ").strip()

    lesson = ask_model(
        f"Teach me {topic}. End with one knowledge-check question"
    )

    print("\n=====LESSON=====\n")
    print(lesson)

    learner_answer = input("\nYour answer:").strip()

    evaluation=evaluate_answer(
        topic,
        lesson,
        learner_answer
    )

    state = {
        "topic": topic,
        "learner_answer": learner_answer,
        "evaluation": evaluation.model_dump(),
        "attempts":1,
        "max_attempts":3,
        "errors":[]
    }

    decision = should_continue(state)

    print("\n=====EVALUATION=====")
    print(evaluation)
    print("\nNext action:",decision)
