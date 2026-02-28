"""
LearnSphere — Image Utility Module
Generates educational visuals using Gemini's image generation capabilities.
"""

import os
import time
import io
import base64
from PIL import Image
from google import genai
from dotenv import load_dotenv

load_dotenv()

_gemini_client = None


def _get_gemini_client():
    """Singleton Google Gemini client (separate from the Cerebras client in genai_utils)."""
    global _gemini_client
    if _gemini_client is None:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError(
                "Please set your GOOGLE_API_KEY in the .env file for image generation"
            )
        _gemini_client = genai.Client(api_key=api_key)
    return _gemini_client


IMAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "generated_images")


def ensure_image_dir():
    """Create image output directory if it doesn't exist."""
    os.makedirs(IMAGE_DIR, exist_ok=True)


def generate_visual(topic):
    """
    Generate an educational diagram/visual for the given ML topic.
    Returns (image_path, description) tuple.
    """
    ensure_image_dir()

    client = _get_gemini_client()

    prompt = f"""Generate a clean, professional educational diagram or infographic about "{topic}" in machine learning.

The image should:
- Have a clean white background
- Use modern, vibrant colors for different elements
- Include clear labels and annotations
- Show key concepts, relationships, or data flow
- Be suitable for a student learning this topic
- Be visually organized with a logical layout

Style: technical infographic, educational poster, clean and modern design.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
            ),
        )

        image_path = None
        description = ""

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                # Save the image
                image_data = part.inline_data.data
                img = Image.open(io.BytesIO(image_data))

                safe_name = "".join(c if c.isalnum() or c in "-_ " else "" for c in topic).strip().replace(" ", "_")
                timestamp = int(time.time())
                filename = f"{safe_name}_{timestamp}.png"
                filepath = os.path.join(IMAGE_DIR, filename)
                img.save(filepath)
                image_path = filepath
            elif part.text is not None:
                description = part.text

        if image_path:
            return image_path, description
        else:
            return None, "Image generation did not return an image. Please try again."

    except Exception as e:
        return None, f"Image generation failed: {str(e)}"


def image_to_base64(image_path):
    """Convert an image file to a base64-encoded string for display."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
