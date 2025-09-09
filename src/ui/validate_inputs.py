from gradio import update
from typing import Any
from src.ui.state import get_qas


def inputs_complete(a: str, b: str, c: str) -> bool:
    placeholders: list[str] = [list(item.values())[0] for item in get_qas()]
    vals: list[str] = [a, b, c]
    for v, p in zip(vals, placeholders):
        if not v or not str(v).strip() or str(v).strip() == str(p).strip():
            return False
    return True


def validate_inputs(a: str, b: str, c: str) -> dict[str, Any]:
    return update(interactive=inputs_complete(a, b, c))
