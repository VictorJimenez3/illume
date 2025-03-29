# ---
# cmd: ["modal", "run", "--detach", "llm_engineering/models/mochi_client.py", "--num-inference-steps", "64"]
# ---

import string
import time
from pathlib import Path

import modal
import boto3

app = modal.App()

image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("git")
    .pip_install(
        "torch==2.5.1",
        "accelerate==1.1.1",
        "hf_transfer==0.1.8",
        "sentencepiece==0.2.0",
        "imageio==2.36.0",
        "imageio-ffmpeg==0.5.1",
        "git+https://github.com/huggingface/transformers@30335093276212ce74938bdfd85bfd5df31a668a",
        "git+https://github.com/huggingface/diffusers@99c0483b67427de467f11aa35d54678fd36a7ea2",
    )
    .env(
        {
            "HF_HUB_ENABLE_HF_TRANSFER": "1",
            "HF_HOME": "/models",
        }
    )
)

# ## Saving outputs

# On Modal, we save large or expensive-to-compute data to
# [distributed Volumes](https://modal.com/docs/guide/volumes)

# We'll use this for saving our Mochi weights, as well as our video outputs.

VOLUME_NAME = "mochi-outputs"
outputs = modal.Volume.from_name(VOLUME_NAME, create_if_missing=True)
OUTPUTS_PATH = Path("/outputs")  # remote path for saving video outputs

MODEL_VOLUME_NAME = "mochi-model"
model = modal.Volume.from_name(MODEL_VOLUME_NAME, create_if_missing=True)
MODEL_PATH = Path("/models")  # remote path for saving model weights

MINUTES = 60
HOURS = 60 * MINUTES

## Downloading the model


with image.imports():
    import torch
    from diffusers import MochiPipeline
    from diffusers.utils import export_to_video


@app.function(
    image=image,
    volumes={
        MODEL_PATH: model,
    },
    timeout=20 * MINUTES,
)
def download_model(revision="83359d26a7e2bbe200ecbfda8ebff850fd03b545"):
    # uses HF_HOME to point download to the model volume
    MochiPipeline.from_pretrained(
        "genmo/mochi-1-preview",
        torch_dtype=torch.bfloat16,
        revision=revision,
    )


## Setting up our Mochi class

# We configure it to use our image, the distributed volume, and a single H100 GPU.
@app.cls(
    image=image,
    volumes={
        OUTPUTS_PATH: outputs,  # videos will be saved to a distributed volume
        MODEL_PATH: model,
    },
    gpu="H100",
    timeout=1 * HOURS,
)
class Mochi:
    @modal.enter()
    def load_model(self):
        # our HF_HOME env var points to the model volume as the cache
        self.pipe = MochiPipeline.from_pretrained(
            "genmo/mochi-1-preview",
            torch_dtype=torch.bfloat16,
        )
        self.pipe.enable_model_cpu_offload()
        self.pipe.enable_vae_tiling()

    @modal.method()
    def generate(
        self,
        prompt,
        negative_prompt="",
        num_inference_steps=200,
        guidance_scale=4.5,
        num_frames=19,
    ):
        frames = self.pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            num_frames=num_frames,
        ).frames[0]

        # save to disk using prompt as filename
        mp4_name = slugify(prompt)
        export_to_video(frames, Path(OUTPUTS_PATH) / mp4_name)
        outputs.commit()
        return mp4_name


## Running Mochi inference

# You can trigger it with:
# ```bash
# modal run --detach mochi
# ```

# Optional command line flags can be viewed with:
# ```bash
# modal run mochi --help
# ```

# Using these flags, you can tweak your generation from the command line:
# ```bash
# modal run --detach mochi --prompt="a cat playing drums in a jazz ensemble" --num-inference-steps=64
# ```


@app.local_entrypoint()
def main(
    prompt="Close-up of a chameleon's eye, with its scaly skin changing color. Ultra high resolution 4k.",
    negative_prompt="",
    num_inference_steps=200,
    guidance_scale=4.5,
    num_frames=19,  # produces ~1s of video
):
    mochi = Mochi()
    mp4_name = mochi.generate.remote(
        prompt=str(prompt),
        negative_prompt=str(negative_prompt),
        num_inference_steps=int(num_inference_steps),
        guidance_scale=float(guidance_scale),
        num_frames=int(num_frames),
    )
    print(f"🍡 video saved to volume at {mp4_name}")

    local_dir = Path("/tmp/mochi")
    local_dir.mkdir(exist_ok=True, parents=True)
    local_path = local_dir / mp4_name
    local_path.write_bytes(b"".join(outputs.read_file(mp4_name)))
    print(f"🍡 video saved locally at {local_path}")

    # Upload the video to S3
    bucket_name = "your-bucket-name"  # Replace with your actual bucket name
    s3_client = boto3.client('s3')
    s3_client.upload_file(local_path, bucket_name, mp4_name)
    
    # Generate a presigned URL that's valid for 1 hour (3600 seconds)
    presigned_url = s3_client.generate_presigned_url('get_object',
        Params={'Bucket': bucket_name, 'Key': mp4_name},
        ExpiresIn=3600
    )
    print(f"🍡 video available at: {presigned_url}")


# ## Addenda

# The remainder of the code in this file is utility code.


def slugify(prompt):
    for char in string.punctuation:
        prompt = prompt.replace(char, "")
    prompt = prompt.replace(" ", "_")
    prompt = prompt[:230]  # since filenames can't be longer than 255 characters
    mp4_name = str(int(time.time())) + "_" + prompt + ".mp4"
    return mp4_name