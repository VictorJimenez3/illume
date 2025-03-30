import os
import requests
from pathlib import Path
from tqdm import tqdm

def download_file(url: str, destination: str):
    """Download a file with progress bar."""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(destination, 'wb') as file, tqdm(
        desc=os.path.basename(destination),
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            pbar.update(size)

def main():
    # Create model directories if they don't exist
    clip_dir = Path.home() / '.cache' / 'ComfyUI' / 'models' / 'clip'
    checkpoints_dir = Path.home() / '.cache' / 'ComfyUI' / 'models' / 'checkpoints'
    
    clip_dir.mkdir(parents=True, exist_ok=True)
    checkpoints_dir.mkdir(parents=True, exist_ok=True)
    
    # Download CLIP model
    clip_url = "https://huggingface.co/openai/clip-vit-large-patch14/resolve/main/pytorch_model.bin"
    clip_path = clip_dir / "clip_vit_h.safetensors"
    
    if not clip_path.exists():
        print("Downloading CLIP model...")
        download_file(clip_url, clip_path)
    else:
        print("CLIP model already exists")
    
    # Download Stable Diffusion model
    sd_url = "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned.safetensors"
    sd_path = checkpoints_dir / "model.safetensors"
    
    if not sd_path.exists():
        print("Downloading Stable Diffusion model...")
        download_file(sd_url, sd_path)
    else:
        print("Stable Diffusion model already exists")
    
    print("\nDownload complete! Models are located at:")
    print(f"CLIP model: {clip_path}")
    print(f"Stable Diffusion model: {sd_path}")

if __name__ == "__main__":
    main() 