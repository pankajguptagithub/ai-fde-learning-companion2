from openai import OpenAI

from companion.config import settings
from companion.prompts import TUTOR_SYSTEM
from companion.context import build_context

client = OpenAI(api_key=settings.openai_api_key)

def ask_model(user_text: str) -> str:
    profile = {
        "goal": "AI FDE",
        "strengths": ["Golang","System Design"],
        "gaps": ["RAG"]
    }
    session = {
        "topic": user_text,
        "attempts": 0
    }
    chunks =  [
        {
            "id": "1",
            "text": "RAG stands for Retrieval Augmented Generation"
        }
        ]

    context = build_context(
        profile,
        session,
        chunks,
        user_text
    )

    print(context)

    response = client.responses.create(
            model=settings.openai_model,
            instructions=(
                "You are a concise AI engineering tutor"
                "Explain with one example and one check-for-understanding question"
                ),
            input=f"""
        {context.learner}
        {context.session}
        {context.evidence}
        {context.task}
            """
            )
    return response.output_text

def safe_ask(user_text: str) -> str:
    try:
        return ask_model(user_text)
    except Exception as exc:
        #During development, log class and request id if available
        raise RuntimeError("Model request failed") from exc

#client = OpenAI()
#response = client.responses.parse(
#    model = settings.openai_model,
#    instructions = TUTOR_SYSTEM,
#    input = "Teach reranking to a learner who understands vector search",
#    text_format = TutorTurn,
#)
#turn = response.output_parsed

