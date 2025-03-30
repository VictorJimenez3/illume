import os
import json
import requests
from pathlib import Path
from typing import Optional, Dict, Any

class ComfyUIClient:
    def __init__(self, server_address: str = "http://127.0.0.1:8188"):
        self.server_address = server_address
        self.client_id = self._get_client_id()
        
    def _get_client_id(self) -> str:
        """Get a unique client ID from the ComfyUI server."""
        response = requests.get(f"{self.server_address}/client_id")
        return response.json()["client_id"]
    
    def generate_video(self, prompt: str, duration: int = 4, fps: int = 8) -> str:
        """
        Generate a video using ComfyUI based on the given prompt.
        
        Args:
            prompt (str): The text prompt to generate the video from
            duration (int): Duration of the video in seconds
            fps (int): Frames per second for the video
            
        Returns:
            str: Path to the generated video file
        """
        # Define the workflow
        workflow = {
            "3": {
                "class_type": "CLIPTextEncode",
                "inputs": {
                    "text": prompt,
                    "clip": ["4", 0]
                }
            },
            "4": {
                "class_type": "LoadCLIPModel",
                "inputs": {
                    "clip_name": "clip_vit_h.safetensors"
                }
            },
            "5": {
                "class_type": "EmptyLatentImage",
                "inputs": {
                    "width": 512,
                    "height": 512,
                    "batch_size": duration * fps
                }
            },
            "6": {
                "class_type": "KSampler",
                "inputs": {
                    "seed": 123456789,
                    "steps": 20,
                    "cfg": 7,
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "denoise": 1,
                    "model": ["7", 0],
                    "positive": ["3", 0],
                    "negative": ["8", 0],
                    "latent_image": ["5", 0]
                }
            },
            "7": {
                "class_type": "LoadModel",
                "inputs": {
                    "model_name": "model.safetensors"
                }
            },
            "8": {
                "class_type": "CLIPTextEncode",
                "inputs": {
                    "text": "blurry, bad quality, distorted",
                    "clip": ["4", 0]
                }
            },
            "9": {
                "class_type": "VAEDecode",
                "inputs": {
                    "samples": ["6", 0],
                    "vae": ["7", 2]
                }
            },
            "10": {
                "class_type": "SaveVideo",
                "inputs": {
                    "images": ["9", 0],
                    "fps": fps
                }
            }
        }
        
        # Queue the workflow
        response = requests.post(
            f"{self.server_address}/prompt",
            json={
                "prompt": workflow,
                "client_id": self.client_id
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to queue workflow: {response.text}")
            
        # Wait for the video to be generated
        while True:
            response = requests.get(f"{self.server_address}/history")
            if response.status_code == 200:
                history = response.json()
                if "10" in history:  # Check if SaveVideo node is complete
                    return history["10"]["outputs"]["video"][0]
            time.sleep(1) 