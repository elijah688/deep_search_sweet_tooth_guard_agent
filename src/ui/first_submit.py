from src.refiner.runner import RefiningAgentRunner
from typing import Optional, Tuple
from src.refiner.types import RefiningResponse
from typing import Callable, Any
from gradio import update
from typing import List


async def first_submit(
    user_input: str,
    gr_update_fn: Callable[..., dict[str, Any]] = update,
    refining_agent: RefiningAgentRunner | None = None,
    update_qas: Optional[Callable[[List[dict[str, str]]], None]] = None,
    questions_list: List[dict[str, str]] = [],
    warning_msg: str = "⚠️ Whoa! 🍫🍕 Looks like someone’s talking snacks. 🍩🍪 Guardrail engaged! ✅",
):
    yield (
        gr_update_fn(interactive=False),
        gr_update_fn(interactive=False),
        gr_update_fn(interactive=False),
        gr_update_fn(interactive=False),
        gr_update_fn(interactive=False),
        gr_update_fn(interactive=False),
        gr_update_fn(interactive=False),
        gr_update_fn(),
        gr_update_fn(interactive=False),
    )

    trying_to_over_eat = False
    if refining_agent:
        res: Tuple[bool, Optional[RefiningResponse]] = await refining_agent.run(
            user_input
        )

        trying_to_over_eat, ref_res = res
        questions_list = [q.model_dump() for q in ref_res.questions] if ref_res else []

    if update_qas:
        update_qas(questions_list)

    # Overeating branch
    if trying_to_over_eat:
        yield (
            gr_update_fn(value=warning_msg, visible=True),  # warning
            gr_update_fn(visible=False),  # user input
            gr_update_fn(visible=False),  # submit button
            gr_update_fn(visible=False),  # QA1
            gr_update_fn(visible=False),  # QA2
            gr_update_fn(visible=False),  # QA3
            gr_update_fn(visible=False),  # final submit
            gr_update_fn(value=""),  # output
            gr_update_fn(visible=True, interactive=True),  # retry button
        )
        return

    # If no agent, provide placeholder QA

    labels = [item["question"] for item in questions_list]
    placeholders = [item["reason"] for item in questions_list]

    updates = [
        gr_update_fn(visible=False),  # hide warning
        gr_update_fn(interactive=False),  # lock user input
        gr_update_fn(interactive=False),  # lock submit button
    ]

    # Populate QA inputs
    for i in range(len(questions_list)):
        updates.append(
            gr_update_fn(
                visible=True,
                label=labels[i],
                placeholder=placeholders[i],
                interactive=True,
                value="",
            )
        )

    # Final submit + output + retry hidden
    updates.extend(
        [
            gr_update_fn(visible=True, interactive=False),  # final submit
            gr_update_fn(visible=False, value=""),  # output hidden
            gr_update_fn(visible=False),  # retry hidden
        ]
    )

    yield tuple(updates)
