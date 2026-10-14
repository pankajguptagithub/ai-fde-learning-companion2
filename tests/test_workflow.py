from companion.workflow import should_continue
from companion.workflow import load_context

def test_max_attempts_exit(monkeypatch):
    state = {
        "topic" : "reranking", "attempts":3, "max_attempts":3,
        "evaluation": {"score":0.2},"errors":[]
    }
    assert should_continue(state) == "stop"

def test_mastery_advances():
    state = {"attempts":1, "max_attempts":3,
            "evaluation": {"score": 0.9}, "errors":[]
            }
    assert should_continue(state) == "advance"
