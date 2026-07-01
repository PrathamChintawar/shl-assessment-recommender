"""
conversation.py

Extracts structured information from the conversation history.

The API is stateless, so every request contains the entire
conversation. This module reconstructs the user's intent.
"""

import re
from typing import Dict, List


SENIORITY = {
    "entry": ["entry", "entry level", "graduate", "fresher", "intern"],
    "mid": ["mid", "mid-level", "3 years", "4 years", "5 years"],
    "senior": ["senior", "lead", "principal", "architect", "manager"]
}


PERSONALITY_WORDS = [
    "personality",
    "behaviour",
    "behavior",
    "opq"
]


COMPARISON_WORDS = [
    "compare",
    "difference",
    "vs",
    "versus"
]


def extract_state(messages: List[Dict]) -> Dict:
    """
    Extract structured state from the full conversation.
    """

    text = " ".join(
        m["content"] for m in messages if m["role"] == "user"
    ).lower()

    state = {
    "role": None,
    "seniority": None,
    "personality": False,
    "comparison": False,
    "compare_names": [],
    "skills": [],
    "messages": messages
}

    # -------- Role Detection --------

    role_patterns = [
        r"java developer",
        r"python developer",
        r"sales",
        r"manager",
        r"data scientist",
        r"analyst",
        r"developer",
        r"engineer"
    ]

    for pattern in role_patterns:
        if pattern in text:
            state["role"] = pattern.title()
            break

    # -------- Seniority --------

    for level, words in SENIORITY.items():
        if any(word in text for word in words):
            state["seniority"] = level
            break

    # -------- Personality --------

    if any(word in text for word in PERSONALITY_WORDS):
        state["personality"] = True

    # -------- Comparison --------

    if any(word in text for word in COMPARISON_WORDS):

        state["comparison"] = True

        assessments = re.findall(
            r"[A-Za-z0-9\-\(\) ]+",
            text
        )

        state["compare_names"] = [
            a.strip() for a in assessments if len(a.strip()) > 3
        ]

    return state


def need_clarification(state: Dict) -> bool:
    """
    Determine if enough information exists.
    """

    if state["comparison"]:
        return False

    if state["role"] is None:
        return True

    if state["seniority"] is None:
        return True

    return False


def clarification_question(state: Dict) -> str:
    """
    Ask the next clarification question.
    """

    if state["role"] is None:
        return "What role are you hiring for?"

    if state["seniority"] is None:
        return "What is the seniority level of the role?"

    return "Could you provide more details?"