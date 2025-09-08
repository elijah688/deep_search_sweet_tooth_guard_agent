import gradio as gr
from fpdf import FPDF
from agents import Runner, InputGuardrailTripwireTriggered
import json
from src.ui.first_submit import first_submit as fs

from src.refiner.refiner import refining_agent, RefiningResponse

DEFAULT_QA = [
    {"question": "", "reason": ""},
    {"question": "", "reason": ""},
    {"question": "", "reason": ""},
]

re_out = "research out"


async def fs_wrapper(user_input):
    async for update in fs(
        gr=gr,
        user_input=user_input,
        agent=refining_agent,
        questions_list=DEFAULT_QA,
    ):
        yield update


def check_inputs(a, b, c):
    placeholders = [list(item.values())[0] for item in DEFAULT_QA]
    vals = [a, b, c]

    for v, p in zip(vals, placeholders):
        if not v or not str(v).strip() or str(v).strip() == str(p).strip():
            return gr.update(interactive=False)
    return gr.update(interactive=True)


def final_submit(a, b, c):
    placeholders = [list(item.values())[0] for item in DEFAULT_QA]
    vals = [a, b, c]
    for v, p in zip(vals, placeholders):
        if not v or not str(v).strip() or str(v).strip() == str(p).strip():
            return gr.update(value="Fill all fields with your own values", visible=True)
    return gr.update(value=re_out, visible=True)


# Function to create PDF
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    filename = "output.pdf"
    pdf.output(filename)
    return filename  # Gradio will use this for download


def reset_app():
    return (
        gr.update(value="", visible=False, interactive=True),  # warning
        gr.update(value="", visible=True, interactive=True),  # user_input
        gr.update(visible=True, interactive=True),  # submit button
        gr.update(visible=False),  # QA1
        gr.update(visible=False),  # QA2
        gr.update(visible=False),  # QA3
        gr.update(visible=False, interactive=False),  # final button
        gr.update(value="", visible=False),  # output
        gr.update(visible=False),  # retry button
        gr.update(value=None, visible=False),  # download button
    )


with gr.Blocks() as demo:
    user_input = gr.Textbox(label="Initial Input")
    submit_btn = gr.Button("Submit")
    warning = gr.Textbox(label="", interactive=False, visible=False)
    qa_inputs = [gr.Textbox(visible=False) for _ in range(3)]
    final_btn = gr.Button("Final Submit", visible=False, interactive=False)
    output = gr.Textbox(label="Output", interactive=False, visible=False)
    download_btn = gr.File(label="Download PDF", visible=False)
    retry_btn = gr.Button("Retry", visible=False)

    # First submit
    submit_btn.click(
        fn=fs_wrapper,
        inputs=[user_input],
        outputs=[
            warning,
            user_input,
            submit_btn,
            qa_inputs[0],
            qa_inputs[1],
            qa_inputs[2],
            final_btn,
            output,
            retry_btn,
        ],
    )

    for box in qa_inputs:
        box.change(fn=check_inputs, inputs=qa_inputs, outputs=final_btn)

    # Final submit with PDF and lock button
    def final_submit_with_download(a, b, c):
        out_update = final_submit(a, b, c)
        final_btn_update = gr.update(interactive=False)

        if out_update["value"] != "Fill all fields with your own values":
            pdf_file = create_pdf(out_update["value"])
            return (
                out_update,
                gr.update(value=pdf_file, visible=True),
                final_btn_update,
                gr.update(visible=True),
            )
        return (
            out_update,
            gr.update(visible=False),
            final_btn_update,
            gr.update(visible=False),
        )

    final_btn.click(
        fn=final_submit_with_download,
        inputs=qa_inputs,
        outputs=[output, download_btn, final_btn, retry_btn],
    )

    # Retry button resets the app
    retry_btn.click(
        fn=reset_app,
        inputs=[],
        outputs=[
            warning,
            user_input,
            submit_btn,
            qa_inputs[0],
            qa_inputs[1],
            qa_inputs[2],
            final_btn,
            output,
            retry_btn,
            download_btn,
        ],
    )

if __name__ == "__main__":
    demo.launch()
