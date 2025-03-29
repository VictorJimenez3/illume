import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from google import genai


class GeminiClient:
    def __init__(self):
        # Get the project root directory (3 levels up from this file)
        project_root = Path(__file__).parent.parent.parent
        # Load the .env file from the project root
        load_dotenv(project_root / '.env')
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        self.client = genai.Client(api_key=api_key)
    
    def generate_text(self, prompt: str, max_tokens: Optional[int] = None) -> str:
        """
        Generate text using the Gemini API.
        
        Args:
            prompt (str): The input prompt
            max_tokens (Optional[int]): Maximum number of tokens to generate
            
        Returns:
            str: Generated text
        """
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text
    
    def generate_stream(self, prompt: str, max_tokens: Optional[int] = None):
        """
        Generate text stream using the Gemini API.
        
        Args:
            prompt (str): The input prompt
            max_tokens (Optional[int]): Maximum number of tokens to generate
            
        Yields:
            str: Generated text chunks
        """
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            stream=True
        )
        for chunk in response:
            yield chunk.text

    def close(self):
        """
        Close the Gemini client session and clean up resources.
        """
        # The Google Generative AI client doesn't require explicit cleanup
        # but we'll keep this method for consistency and future-proofing
        pass 