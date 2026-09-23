from __future__ import annotations

import gradio as gr

from ajvyra_ai_video_generation_core_v1 import (
    generate_anime_video,
)
from ajvyra_ai_video_library_store_v1 import (
    AJVYRAAIVideoLibrary,
)


library = AJVYRAAIVideoLibrary()


def generate_from_prompt(
    prompt: str,
    frames: int,
    steps: int,
    seed: int,
):
    if not prompt or not prompt.strip():
        return (
            None,
            "Please describe the anime scene you want.",
        )

    try:
        video_path = generate_anime_video(
            prompt=prompt,
            num_frames=int(frames),
            inference_steps=int(steps),
            seed=int(seed) if int(seed) >= 0 else None,
        )

        # The local path is kept in the catalog.
        # A persistent/public URL can be attached later
        # by the storage publisher.
        item = library.add_video(
            prompt=prompt.strip(),
            video_url=video_path,
            local_path=video_path,
            title="AJVYRA AI Creation",
        )

        library.export_site_catalog()

        return (
            video_path,
            f"READY • {item['id']}",
        )

    except Exception as exc:
        return (
            None,
            f"Generation failed: {exc}",
        )


CSS = """
body {
    background: #050505 !important;
}

.gradio-container {
    max-width: 980px !important;
    background: #050505 !important;
    color: #f5f5f5 !important;
}

#ajv-title {
    text-align: center;
    margin-bottom: 8px;
}

#ajv-subtitle {
    text-align: center;
    color: #8d8d8d;
    margin-bottom: 24px;
}

button {
    border-radius: 14px !important;
}

textarea {
    background: #0c0c0c !important;
    color: #f5f5f5 !important;
    border: 1px solid #242424 !important;
}
"""


with gr.Blocks(
    title="AJVYRA AI Video Studio",
    css=CSS,
) as demo:

    gr.Markdown(
        "# 🦊 AJVYRA AI VIDEO",
        elem_id="ajv-title",
    )

    gr.Markdown(
        "Create an original animated/anime scene from text.",
        elem_id="ajv-subtitle",
    )

    with gr.Row():

        with gr.Column(scale=2):

            prompt = gr.Textbox(
                label="Describe your scene",
                placeholder=(
                    "A white-haired anime boy walking alone "
                    "through a rainy neon city at night..."
                ),
                lines=6,
            )

            frames = gr.Slider(
                minimum=17,
                maximum=81,
                value=49,
                step=8,
                label="Frames",
            )

            steps = gr.Slider(
                minimum=8,
                maximum=40,
                value=20,
                step=1,
                label="Inference steps",
            )

            seed = gr.Number(
                value=-1,
                precision=0,
                label="Seed (-1 = random)",
            )

            generate = gr.Button(
                "✦ Generate Anime Video",
                variant="primary",
            )

            status = gr.Markdown(
                "Waiting for a prompt..."
            )

        with gr.Column(scale=3):

            video = gr.Video(
                label="Generated Video",
                autoplay=False,
            )

    generate.click(
        fn=generate_from_prompt,
        inputs=[
            prompt,
            frames,
            steps,
            seed,
        ],
        outputs=[
            video,
            status,
        ],
    )


if __name__ == "__main__":
    demo.queue(
        max_size=32,
        default_concurrency_limit=1,
    ).launch(
        max_file_size="50mb",
    )
