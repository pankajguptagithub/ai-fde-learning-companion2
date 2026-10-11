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
