"""Text-to-Speech agent — converts text into audio via ElevenLabs."""

from pathlib import Path

from agents.client import get_client
from agents.config import get_settings


def text_to_speech(
    text: str,
    *,
    output_path: str | Path | None = None,
    voice_id: str | None = None,
    model_id: str | None = None,
    output_format: str | None = None,
) -> Path:
    """
    Convert text to speech and save as an audio file.

    Returns the path to the saved file.
    """
    if not text.strip():
        raise ValueError("Text cannot be empty.")

    settings = get_settings()
    out = Path(output_path or settings.default_speech_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    client = get_client()
    audio_stream = client.text_to_speech.convert(
        voice_id=voice_id or settings.voice_id,
        text=text,
        model_id=model_id or settings.tts_model,
        output_format=output_format or settings.tts_output_format,
    )

    with out.open("wb") as f:
        for chunk in audio_stream:
            f.write(chunk)

    return out
