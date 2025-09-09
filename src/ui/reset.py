from gradio import update


def reset_app():
    return (
        update(value="", visible=False, interactive=True),  # warning
        update(value="", visible=True, interactive=True),  # user_input
        update(visible=True, interactive=True),  # submit button
        update(visible=False),  # QA1
        update(visible=False),  # QA2
        update(visible=False),  # QA3
        update(visible=False, interactive=False),  # final button
        update(value="", visible=False),  # output
        update(visible=False),  # retry button
        update(value=None, visible=False),  # download button
    )
