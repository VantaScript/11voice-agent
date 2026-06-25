"""End-to-end pipelines combining TTS and STT agents."""

from dataclasses import dataclass
from pathlib import Path
import re

from agents.config import get_settings
from agents.stt_agent import TranscriptionResult, speech_to_text
from agents.tts_agent import text_to_speech


@dataclass
class RoundtripResult:
    """Result of a text → speech → text round-trip."""

    original: str
    transcript: str
    audio_path: Path
    language_code: str | None = None
    language_probability: float | None = None

    @property
    def matches(self) -> bool:
        return _normalize(self.original) == _normalize(self.transcript)


def _normalize(text: str) -> str:
    """Loose comparison: lowercase, strip punctuation, collapse whitespace."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def roundtrip(
    text: str,
    *,
    output_path: str | Path | None = None,
    language_code: str | None = None,
) -> RoundtripResult:
    """
    Run text through TTS, then transcribe the audio with STT.

    Returns original text, transcript, and the generated audio path.
    """
    settings = get_settings()
    audio_path = text_to_speech(
        text,
        output_path=output_path or settings.output_dir / "roundtrip.mp3",
    )
    transcription: TranscriptionResult = speech_to_text(
        audio_path,
        language_code=language_code,
    )
    return RoundtripResult(
        original=text,
        transcript=transcription.text,
        audio_path=audio_path,
        language_code=transcription.language_code,
        language_probability=transcription.language_probability,
    )
