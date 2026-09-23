from __future__ import annotations

import gradio as gr

from ajvyra_ai_video_studio_controller_v2 import (
    AJVYRAAIVideoStudioController,
)


studio = (
    AJVYRAAIVideoStudioController()
)


def create_video(
    prompt: str,
    session_id: str,
):

    if not prompt or not prompt.strip():
        return (
            None,
            "❌ Please describe an anime scene.",
        )

    try:

        result = studio.create_video(
            prompt=prompt,
            session_id=session_id,
        )

        if result["status"] != "ready":

            return (
                None,
                "❌ Generation failed:\n\n"
                + str(
                    result.get(
                        "error",
                        "Unknown error",
                    )
                ),
            )

        return (
            result["video_url"],
            (
                "## ✅ Video Ready\n\n"
                f"`{result['job_id']}`\n\n"
                "The video has been published "
                "to the AJVYRA AI Community feed."
            ),
        )

    except Exception as exc:

        return (
            None,
            (
                "## ⚠️ AJVYRA AI\n\n"
                f"{exc}"
            ),
        )


def generate_session_id():
    import secrets

    return (
        "browser-"
        + secrets.token_hex(12)
    )


with gr.Blocks(
    title="AJVYRA AI Video Studio"
) as demo:

    session_id = gr.State(
        generate_session_id()
    )

    gr.Markdown(
        """
# 🦊 AJVYRA AI VIDEO

### Create an anime video from text.

Write the scene you imagine.
AJVYRA converts it into an animated video
and publishes the finished result to the
AI Community section.
"""
    )

    with gr.Row():

        with gr.Column(
            scale=2
        ):

            prompt = gr.Textbox(
                label="Your prompt",
                placeholder=(
                    "A white-haired anime boy "
                    "walking alone through a "
                    "rainy neon city at night, "
                    "cinematic and emotional..."
                ),
                lines=7,
                max_lines=12,
            )

            generate = gr.Button(
                "✦ Generate Anime Video",
                variant="primary",
            )

            gr.Markdown(
                """
**Only animated/anime output is supported.**

The service may place your request in a
GPU queue because the free AI infrastructure
has limited capacity.
"""
            )

        with gr.Column(
            scale=3
        ):

            output = gr.Video(
                label="Generated Video",
                interactive=False,
            )

            status = gr.Markdown(
                "Waiting for your prompt..."
            )

    generate.click(
        fn=create_video,
        inputs=[
            prompt,
            session_id,
        ],
        outputs=[
            output,
            status,
        ],
        concurrency_limit=1,
    )


if __name__ == "__main__":

    demo.queue(
        max_size=16,
        default_concurrency_limit=1,
    ).launch(
        show_error=True
    )
