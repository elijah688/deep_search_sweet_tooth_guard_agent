import gradio as gr
import time

qa = [{"q0": "r0"}, {"q1": "r1"}, {"q2": "r2"}]
re_out = "research out"

def first_submit(user_input):
    time.sleep(2)

    labels = [list(item.keys())[0] for item in qa]
    placeholders = [list(item.values())[0] for item in qa]

    user_update = gr.update(interactive=False)
    btn_update = gr.update(interactive=False)

    qa_updates = [
        gr.update(visible=True, label=labels[i], placeholder=placeholders[i], interactive=True, value="")
        for i in range(3)
    ]

    final_update = gr.update(visible=True, interactive=False)
    output_update = gr.update(visible=False, value="")  # keep hidden until final submit

    return user_update, btn_update, qa_updates[0], qa_updates[1], qa_updates[2], final_update, output_update

def check_inputs(a, b, c):
    placeholders = [list(item.values())[0] for item in qa]
    vals = [a, b, c]

    for v, p in zip(vals, placeholders):
        if not v or not str(v).strip() or str(v).strip() == str(p).strip():
            return gr.update(interactive=False)
    return gr.update(interactive=True)

def final_submit(a, b, c):
    placeholders = [list(item.values())[0] for item in qa]
    vals = [a, b, c]
    for v, p in zip(vals, placeholders):
        if not v or not str(v).strip() or str(v).strip() == str(p).strip():
            return gr.update(value="Fill all fields with your own values", visible=True)
    return gr.update(value=re_out, visible=True)

with gr.Blocks() as demo:
    # Input row
    user_input = gr.Textbox(label="Initial Input")
    submit_btn = gr.Button("Submit")

    # QA inputs stacked as rows
    qa_inputs = [gr.Textbox(visible=False) for _ in range(3)]

    # Final submit button and output stacked
    final_btn = gr.Button("Final Submit", visible=False, interactive=False)
    output = gr.Textbox(label="Output", interactive=False, visible=False)

    submit_btn.click(
        fn=first_submit,
        inputs=[user_input],
        outputs=[user_input, submit_btn, qa_inputs[0], qa_inputs[1], qa_inputs[2], final_btn, output],
    )

    for box in qa_inputs:
        box.change(fn=check_inputs, inputs=qa_inputs, outputs=final_btn)

    final_btn.click(fn=final_submit, inputs=qa_inputs, outputs=output)

if __name__ == "__main__":
    demo.launch()
