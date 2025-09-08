from agents import Runner, InputGuardrailTripwireTriggered, Agent
import gradio
import asyncio


DEFAULT_QA = [
    {"question": "q0", "reason": "r0"},
    {"question": "q1", "reason": "r1"},
    {"question": "q2", "reason": "r2"},
]


async def first_submit(
    user_input: str,
    gr: gradio,
    agent: Agent = None,
    questions_list: list[dict[str, str]] = DEFAULT_QA,
    warning_msg: str = "⚠️ Whoa there, Sugar Bear!\n🍰🍫🍕 Slow down! Your sweet tooth is on fire! 🔥🥐🍩",
):
    yield (
        gr.update(interactive=False),
        gr.update(interactive=False),
        gr.update(interactive=False),
        gr.update(interactive=False),
        gr.update(interactive=False),
        gr.update(interactive=False),
        gr.update(interactive=False),
        gr.update(interactive=False),
        gr.update(interactive=False),
    )

    await asyncio.sleep(1)

    agent = None
    trying_to_over_eat = False
    try:
        if agent:
            res = (await Runner.run(agent, input=user_input)).final_output
            questions_list = [x.model_dump() for x in res.questions]
    except InputGuardrailTripwireTriggered:
        trying_to_over_eat = True

    # Overeating branch
    if trying_to_over_eat:
        yield (
            gr.update(value=warning_msg, visible=True),  # warning
            gr.update(visible=False),  # user input
            gr.update(visible=False),  # submit button
            gr.update(visible=False),  # QA1
            gr.update(visible=False),  # QA2
            gr.update(visible=False),  # QA3
            gr.update(visible=False),  # final submit
            gr.update(visible=False, value=""),  # output
            gr.update(visible=True, interactive=True),  # retry button
        )
        return

    # If no agent, provide placeholder QA

    labels = [item["question"] for item in questions_list]
    placeholders = [item["reason"] for item in questions_list]

    updates = [
        gr.update(visible=False),  # hide warning
        gr.update(interactive=False),  # lock user input
        gr.update(interactive=False),  # lock submit button
    ]

    # Populate QA inputs
    for i in range(len(questions_list)):
        updates.append(
            gr.update(
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
            gr.update(visible=True, interactive=False),  # final submit
            gr.update(visible=False, value=""),  # output hidden
            gr.update(visible=False),  # retry hidden
        ]
    )

    yield tuple(updates)
