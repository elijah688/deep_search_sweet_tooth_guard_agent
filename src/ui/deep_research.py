from src.ui.validate_inputs import inputs_complete
from gradio import update
from src.ui.state import research_output
from typing import Any
from src.ui.create_pdf import create_pdf


def __launch_deep_research(a: str, b: str, c: str) -> dict[str, Any]:
    if not inputs_complete(a, b, c):
        return update(value="Fill all fields with your own values", visible=True)
    return update(value=research_output, visible=True)


def submit_deep_research(a: str, b: str, c: str):
    out_update = __launch_deep_research(a, b, c)
    final_btn_update = update(interactive=False)

    if out_update["value"] != "Fill all fields with your own values":
        pdf_file = create_pdf(out_update["value"])
        return (
            out_update,
            update(value=pdf_file, visible=True),
            final_btn_update,
            update(visible=True, interactive=True),
        )
    return (
        out_update,
        update(visible=False),
        final_btn_update,
        update(visible=False),
    )
