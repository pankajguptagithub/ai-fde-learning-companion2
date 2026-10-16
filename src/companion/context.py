from dataclasses import dataclass

@dataclass(frozen=True)
class ContextPacket:
    learner: str
    session: str
    evidence: str
    history: str
    task: str


def build_context(
        profile: dict, 
        session: dict,
        chunks: list[dict],
        attempts: list[dict],
        task: str
        )-> ContextPacket:
    strengths = ", ".join(profile.get("strengths",[])[:5]) or "unknown"
    gaps = ", ".join(profile.get("gaps",[])[:5]) or "unknown"
    learner = (
            f"Goal : {profile.get('goal','AI FDE')}\n"
            f"Strengths: {strengths}\n"
            f"Gaps: {gaps}"
            )
    session_text = (
            f"Topic: {session['topic']}\n"
            f"Attempts: {session.get('attempts',0)}"
            )
    evidence = "\n\n".join(
                f"[{c['id']}]{c['text']}" for c in chunks[:4]
            ) or "No evidence supplied."
    history = "\n".join(
            f"Attempt score: {a['score']}"
            for a in attempts
    ) or "No previous learning attempts"
    return ContextPacket(
            learner,
            session_text,
            evidence,
            history,
            task
            )
