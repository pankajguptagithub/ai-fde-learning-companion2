from companion.agent import agent

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Use the get_learning_profile tool"
                    "to retreive the profile for user123"
                    )    
    }]
})

for message in result["messages"]:
    print(type(message).__name__,":",message.content)
