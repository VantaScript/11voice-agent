"""Speech-to-Text agent — transcribes audio via ElevenLabs Scribe."""

from dataclasses import dataclass
from pathlib import Path

from elevenlabs.core.api_error import ApiError

from agents.client import get_client
from agents.config import get_settings
from agents.errors import AudioNotFoundError, wrap_api_error


@dataclass
class TranscriptionResult:
    """Transcription output from the STT agent."""

    text: str
    language_code: str | None = None
    language_probability: float | None = None


def speech_to_text(
    audio_path: str | Path,
    *,
    model_id: str | None = None,
    language_code: str | None = None,
    diarize: bool = False,
    tag_audio_events: bool = False,
) -> TranscriptionResult:
    """
    Transcribe an audio file to text.

    Supports MP3, WAV, MP4, and other common formats.
    """
    path = Path(audio_path)
    if not path.is_file():
        raise AudioNotFoundError(f"Audio file not found: {path}")

    settings = get_settings()
    client = get_client()
    try:
        with path.open("rb") as audio_file:
            result = client.speech_to_text.convert(
                file=audio_file,
                model_id=model_id or settings.stt_model,
                language_code=language_code,
                diarize=diarize,
                tag_audio_events=tag_audio_events,
            )
    except ApiError as err:
        raise wrap_api_error(err) from err

    return TranscriptionResult(
        text=result.text,
        language_code=getattr(result, "language_code", None),
        language_probability=getattr(result, "language_probability", None),
    )
