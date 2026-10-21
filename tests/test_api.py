from fastapi.testclient import TestClient
from companion.api import app

client = TestClient(app)

def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status":"ok"}

def test_learn_success():
    response = client.post(
        "/learn",
        json = {
            "user_id" : "phase9_test_user",
            "topic" : "RAG",
            "mode" : "quiz",
            "learner_answers" : [
                "RAG combines retrieval and generation",
            ],
            "max_attempts" : 3,
        },
    )

    assert response.status_code == 200
    
    data = response.json()

    assert data["evaluation"]["score"] == 0.9
    assert data["next_action"] == "advance"

def test_learn_rejects_invalid_mode():
    response = client.post(
        "/learn",
        json={
            "user_id": "phase9_test_user",
            "topic" : "RAG",
            "mode" : "invalid",
            "learner_answers": [],
            "max_attempts" : 3,
        },
    )

    assert response.status_code == 422


def test_learn_rejects_blank_user_id():
    response = client.post(
        "/learn",
        json = {
            "user_id": "",
            "topic": "RAG",
            "mode": "quiz",
            "learner_answers": [],
            "max_attempts": 3,
        },
    )
    assert response.status_code == 422

def test_learn_rejects_blank_topic():
    response = client.post(
        "/learn",
        json = {
            "user_id": "phase9_test_user",
            "topic": "",
            "mode": "quiz",
            "learner_answers": [],
            "max_attempts": 3,
        }
    )
    assert response.status_code == 422
def test_learn_rejects_invalid_max_attempts():
    response = client.post(
        "/learn",
        json = {
            "user_id": "phase9_test_user",
            "topic": "RAG",
            "mode": "quiz",
            "learner_answers": [],
            "max_attempts": 6,
        }
    )
    assert response.status_code == 422
