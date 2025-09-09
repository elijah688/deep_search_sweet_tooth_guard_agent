from typing import List

QESTIONS_ANSWERS: List[dict[str, str]] = [
    {"question": "q1", "reason": "r1"},
    {"question": "q2", "reason": "r2"},
    {"question": "q3", "reason": "r3"},
]


def set_qas(qas: List[dict[str, str]]):
    QESTIONS_ANSWERS.clear()
    QESTIONS_ANSWERS.extend(qas)
    


def get_qas() -> List[dict[str, str]]:
    return QESTIONS_ANSWERS


research_output = "research out"
