import gradio as gr
from src.ui.first_submit import first_submit as fs
from src.refiner.factory import spawn_refining_agent
from src.refiner.runner import RefiningAgentRunner
from src.ui.validate_inputs import validate_inputs
from src.ui.reset import reset_app
from src.ui.deep_research import submit_deep_research
from src.deep_research.manager import DeepResearchManager
from agents import trace

refining_agent = RefiningAgentRunner(spawn_refining_agent())
drm = DeepResearchManager()


async def fs_wrapper(user_input: str):
    async for ui_update in fs(
        user_input=user_input,
        refining_agent=refining_agent,
    ):
        yield ui_update


async def sd_wrapper(user_input: str, a: str, b: str, c: str):
    async for ui_update in submit_deep_research(
        topic=user_input, a=a, b=b, c=c, drm=drm
    ):
        yield ui_update



with gr.Blocks() as demo:
    with trace("Deep Search"):
        user_input = gr.Textbox(label="Initial Input")
        refine_btn = gr.Button("Submit")
        warning = gr.Textbox(label="", interactive=False, visible=False)
        qa_inputs = [gr.Textbox(visible=False) for _ in range(3)]
        deep_search_btn = gr.Button("Final Submit", visible=False, interactive=False)
        output = gr.Markdown(label="Output", visible=False)
        download_btn = gr.File(label="Download PDF", visible=False)
        retry_btn = gr.Button("Retry", visible=False)

        refine_btn.click(
            fn=fs_wrapper,
            inputs=[user_input],
            outputs=[
                warning,
                user_input,
                refine_btn,
                qa_inputs[0],
                qa_inputs[1],
                qa_inputs[2],
                deep_search_btn,
                output,
                retry_btn,
            ],
        )

        for box in qa_inputs:
            box.change(fn=validate_inputs, inputs=qa_inputs, outputs=deep_search_btn)

        deep_search_btn.click(
            fn=sd_wrapper,
            inputs=[user_input, *qa_inputs],
            outputs=[output, download_btn, deep_search_btn, retry_btn],
        )

        retry_btn.click(
            fn=reset_app,
            inputs=[],
            outputs=[
                warning,
                user_input,
                refine_btn,
                qa_inputs[0],
                qa_inputs[1],
                qa_inputs[2],
                deep_search_btn,
                output,
                retry_btn,
                download_btn,
            ],
        )

if __name__ == "__main__":
    demo.launch()
