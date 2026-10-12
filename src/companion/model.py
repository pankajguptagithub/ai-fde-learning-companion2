from openai import OpenAI
from companion.config import settings

client = OpenAI(api_key=settings.openai_api_key)

def ask_model(user_text: str) -> str:
    response = client.responses.create(
            model=settings.openai_model,
            instructions=(
                "You are a concise AI engineering tutor"
                "Explain with one example and one check-for-understanding question"
                ),
            input=user_text,
            )
    return response.output_text

def safe_ask(user_text: str) -> str:
    try:
        return ask_model(user_text)
    except Exception as exc:
        #During development, log class and request id if available
        raise RuntimeError("Model request failed") from exc

client = OpenAI()
response = client.responses.parse(
    model = settings.openai_model,
    instructions = TUTOR_SYSTEM,
    input = "Teach reranking to a learner who understands vector search",
    text_format = TutorTurn,
)
turn = response.output_parsed

