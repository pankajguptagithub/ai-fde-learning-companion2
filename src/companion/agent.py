from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from companion.config import settings

from companion.tools import(
        get_learning_profile,
        save_learning_attempt,
)

model = init_chat_model(
    f"openai:{settings.openai_model}",
    temperature=0,
    api_key=settings.openai_api_key,
)

agent = create_agent(
    model = model,
    tools = [get_learning_profile,save_learning_attempt],
    system_prompt=(
        "You are a bounded learning coach. Use tools only when needed"
        "Never invent profile data. ask before overwriting durable learner facts"
    ),
)

result = agent.invoke({
        "messages": [{"role":"user","content":"Review my weak AI topics"}]
})
