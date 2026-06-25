"""Text-to-Speech agent — converts text into audio via ElevenLabs."""

from pathlib import Path

from agents.client import get_client

# "George" — browse more at https://elevenlabs.io/app/voice-library
DEFAULT_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"
DEFAULT_MODEL_ID = "eleven_flash_v2_5"
DEFAULT_OUTPUT_FORMAT = "mp3_44100_128"


def text_to_speech(
    text: str,
    *,
    output_path: str | Path = "output/speech.mp3",
    voice_id: str = DEFAULT_VOICE_ID,
    model_id: str = DEFAULT_MODEL_ID,
    output_format: str = DEFAULT_OUTPUT_FORMAT,
) -> Path:
    """
    Convert text to speech and save as an audio file.

    Returns the path to the saved file.
    """
    if not text.strip():
        raise ValueError("Text cannot be empty.")

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    client = get_client()
    audio_stream = client.text_to_speech.convert(
        voice_id=voice_id,
        text=text,
        model_id=model_id,
        output_format=output_format,
    )

    with out.open("wb") as f:
        for chunk in audio_stream:
            f.write(chunk)

    return out
