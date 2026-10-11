from companion.prompts import TUTOR_SYSTEM
from companion.schemas import TutorTurn

import pytest
from pydantic import ValidationError

def test_prompt_contains_non_negotiables():
    assert "exactly one diagnostic question" in TUTOR_SYSTEM
    assert "do not invert" in TUTOR_SYSTEM.lower()


def test_tutor_schema_rejects_bad_confidence():
    with pytest.raises(ValidationError):
        TutorTurn(
            concept="RAG",
            explanation="x",
            example="y",
            diagnostic_question="z",
            confidence=1.5,
        )
