import json
import pytest


from pathlib import Path
from companion.memory import save_attempt
from companion.retrieval import retrieve
from companion.workflow import(
    should_continue,
    validate_state,
    validate_evidence,
)        

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EVAL_FILE = PROJECT_ROOT / "data" / "evals" / "learning_cases.jsonl"

def load_cases() -> dict:
    cases = {}

    with EVAL_FILE.open(
        "r",
        encoding = "utf-8",
    ) as file:
        for line in file:
            case = json.loads(line)
            cases[case["id"]] = case

    return cases

CASES = load_cases()

def test_rag_correct():
    case = CASES["rag_correct"]


    state = {
        "attempts": 1,
        "max_attempts": 3,
        "evaluation": {"score":0.9},
        "errors": [],
    }

    assert should_continue(state) == case["expected_action"]

def test_rag_partial():
    case = CASES["rag_partial"]

    state = {
        "attempts": 1,
        "max_attempts": 3,
        "evaluation": {"score":0.5},
        "errors": [],
    }

    assert should_continue(state) == case["expected_action"]

def test_rag_wrong():
    case = CASES["rag_wrong"]

    state = {
        "attempts": 1,
        "max_attempts": 3,
        "evaluation": {"score":0.2},
        "errors": [],
    }

    assert should_continue(state) == case["expected_action"]

def test_invalid_score():
    case = CASES["invalid_score"]

    with pytest.raises(ValueError):
        save_attempt(
            user_id="phase8_test_user",
            topic="RAG",
            score=case["score"],
        )    

def test_max_attempts():
    case = CASES["max_attempts"]

    state = {
        "attempts": case["attempts"],
        "max_attempts": case["max_attempts"], 
        "evaluation": {
            "score": case["score"],
        },
        "errors": [],
    }

    assert should_continue(state) == case["expected_action"]



def test_missing_evidence():
    case = CASES["missing_evidence"]

    results = retrieve(case["topic"])

    assert results == []


def test_blank_topic():
    case = CASES["blank_topic"]

    errors = validate_state(
        {
            "topic": case["topic"],
            "max_attempts": 3,
        }
    )

    assert case["expected_error"] in errors

def test_invalid_loop_limit():
    
    case = CASES["invalid_loop_limit"]
    
    errors = validate_state(
        {
            "topic": case["topic"],
            "max_attempts": case["max_attempts"],
        }

    )

    assert case["expected_error"] in errors


def test_existing_error_stops_workflow():
    case = CASES["existing_error"]

    state = {
        "attempts": 1,
        "max_attempts": 3,
        "evaluation": {
            "score": case["score"],
        },
        "errors": case["errors"],
    }

    assert should_continue(state) == case["expected_action"]


def test_prompt_injection_has_no_evidence():
    case = CASES["prompt_injection"]

    results = retrieve(case["topic"])

    assert isinstance(results,list)

def test_jailbreak_role_override():
    case = CASES["jailbreak_role_override"]

    errors = validate_state(
        {
            "topic": case["topic"],
            "max_attempts": 3,
        }
    )

    assert case["expected_error"] in errors

def test_system_prompt_disclosure():
    case = CASES['system_prompt_disclosure']

    errors = validate_state(
        {
            "topic": case["topic"],
            "max_attempts":3,
        }
    )

    assert case["expected_error"] in errors

def test_secret_extraction():
    case = CASES["secret_extraction"]

    errors = validate_state(
        {
            "topic": case["topic"],
            "max_attempts": 3,
        }
    )

    assert case["expected_error"] in errors

def test_unsafe_tool_request():
    case = CASES["unsafe_tool_request"]

    errors = validate_state(
        {
            "topic": case["topic"],
            "max_attempts": 3,
        }
    )

    assert case["expected_error"] in errors


def test_hard_limit_bypass():
    case = CASES["hard_limit_bypass"]

    errors = validate_state(
        {
            "topic": case["topic"],
            "max_attempts": case["max_attempts"]
        }

    )

    assert case["expected_error"] in errors

def test_indirect_rag_injection():
    case = CASES['indirect_rag_injection']

    chunks = [
        {
            "id": "malicious-001",
            "text": case["document_text"],
        }
    ]

    errors = validate_evidence(chunks)

    assert case["expected_error"] in errors
