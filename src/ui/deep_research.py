from src.ui.validate_inputs import inputs_complete
from gradio import update
from src.ui.create_pdf import create_pdf
from src.ui.state import get_qas
from src.deep_research.web_research_designer.types import (
    ClarifyingQA,
)
from asyncio import sleep

from src.deep_research.manager import DeepResearchManager


import string
import random
from collections.abc import AsyncGenerator


async def submit_deep_research(
    topic: str, a: str, b: str, c: str, drm: DeepResearchManager
):
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

    final_btn_update = update(interactive=False)

    valid_questions = [
        q.get("question") for q in get_qas() if q.get("question") is not None
    ]

    clarifying_qas = [
        ClarifyingQA(question=q, answer=ans)
        for q, ans in zip(valid_questions, [a, b, c])
        if q is not None
    ]
    print(clarifying_qas)

    out: str = ""

    yield (
        update(visible=False),
        update(visible=False),
        update(visible=True, interactive=False),
        update(visible=False),
    )

    # async for c in stream(20,20):
    async for c in drm.stream(topic=topic, clarifying_qas=clarifying_qas):
        out += c
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


async def stream(n_chunks: int, chunk_size: int = 500) -> AsyncGenerator[str, None]:
    chars = string.ascii_letters + string.digits + string.punctuation
    for _ in range(n_chunks):
        chunk = "".join(random.choices(chars, k=chunk_size))
        await sleep(0.1)
        yield chunk
