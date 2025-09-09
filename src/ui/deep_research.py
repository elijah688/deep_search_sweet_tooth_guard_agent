from src.ui.validate_inputs import inputs_complete
from gradio import update
from typing import Any
from src.ui.create_pdf import create_pdf
from src.ui.state import DEFAULT_QA
from src.deep_research.web_research_designer.types import (
    ClarifyingQA,
)
from asyncio import sleep


import string
import random
from collections.abc import AsyncGenerator


from json import dumps


def __launch_deep_research(a: str, b: str, c: str) -> dict[str, Any]:
    if not inputs_complete(a, b, c):
        return update(value="Fill all fields with your own values", visible=True)
    return update(value="", visible=True)


async def submit_deep_research(a: str, b: str, c: str):
    invalid = not inputs_complete(a, b, c)
    if invalid:
        yield (
            update(
                visible=False,
                value="",
            ),
            update(visible=False),
            update(visible=True),
            update(
                visible=False,
            ),
        )
        return

    out_update = __launch_deep_research(a, b, c)
    final_btn_update = update(interactive=False)

    valid_questions = [
        q.get("question") for q in DEFAULT_QA if q.get("question") is not None
    ]

    clarifying_qas = [
        ClarifyingQA(question=q, answer=ans)
        for q, ans in zip(valid_questions, [a, b, c])
        if q is not None
    ]

    print(dumps([x.model_dump() for x in clarifying_qas], indent=4))
    print(out_update)
    out: str = ""
    async for c in random_char_stream(30, 10):
        out += c
        print(c)
        yield (
            update(value=out, visible=True),
            update(visible=False),
            final_btn_update,
            update(visible=False, interactive=False),
        )
    yield (
        update(value=out, visible=True),
        update(value=create_pdf(out), visible=True),
        final_btn_update,
        update(visible=True, interactive=True),
    )


async def random_char_stream(
    n_chunks: int, chunk_size: int = 500
) -> AsyncGenerator[str, None]:
    chars = string.ascii_letters + string.digits + string.punctuation
    for _ in range(n_chunks):
        chunk = "".join(random.choices(chars, k=chunk_size))
        await sleep(0.1)
        yield chunk


# Usage example
async def main():
    async for chunk in random_char_stream(3):
        print(chunk)
