"""
LearnSphere — Audio Utility Module
Converts AI-generated scripts into natural-sounding MP3 audio via edge-tts.
Uses Microsoft Edge's neural TTS voices for human-like speech.
"""

import os
import time
import asyncio
import edge_tts


AUDIO_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "generated_audio")

# Natural-sounding voice options
VOICE = "en-US-AriaNeural"  # Friendly, clear female voice


def ensure_audio_dir():
    """Create audio output directory if it doesn't exist."""
    os.makedirs(AUDIO_DIR, exist_ok=True)


async def _generate_audio_async(text, filepath):
    """Async helper for edge-tts generation."""
    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE,
        rate="-5%",      # Slightly slower for clarity
        pitch="+0Hz",
    )
    await communicate.save(filepath)


def generate_audio(text, topic="lesson"):
    """
    Convert text to an MP3 file using edge-tts (natural neural voice).
    Returns the absolute path to the generated file.
    """
    ensure_audio_dir()
    safe_name = "".join(c if c.isalnum() or c in "-_ " else "" for c in topic).strip().replace(" ", "_")
    timestamp = int(time.time())
    filename = f"{safe_name}_{timestamp}.mp3"
    filepath = os.path.join(AUDIO_DIR, filename)

    # Run the async edge-tts generation
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If we're already in an async context, create a new loop
            import threading
            result = [None]
            def run():
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                new_loop.run_until_complete(_generate_audio_async(text, filepath))
                new_loop.close()
            thread = threading.Thread(target=run)
            thread.start()
            thread.join()
        else:
            loop.run_until_complete(_generate_audio_async(text, filepath))
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(_generate_audio_async(text, filepath))
        loop.close()

    return filepath
