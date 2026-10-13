from langchain.tools import tool

@tool
def get_learning_profile(user_id:str) -> dict:
    """Return the learner profile for one known user id"""
    #return profile_repo.get(user_id)
    return {
        "user_id": user_id,
        "goal": "AI expert fde",
        "strengths": ["Scripting", "System design"],
        "gaps":["RAG","Agentic AI"]
    }

@tool
def save_learning_attempt(user_id:str, topic: str, score:float) -> str:
    """Store one validated learning attempt"""
    if not 0 <= score <= 1:
        raise ValueError("score must be between 0 and 1")
    #attempt_repo.save(user_id,topic,score)
    #return saved
    return f"Saved {topic} score {score} for {user_id}"
