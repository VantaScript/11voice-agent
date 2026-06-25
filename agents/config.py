"""Central configuration for STT and TTS agents."""

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# "George" — https://elevenlabs.io/app/voice-library
DEFAULT_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"
DEFAULT_TTS_MODEL = "eleven_flash_v2_5"
DEFAULT_TTS_OUTPUT_FORMAT = "mp3_44100_128"
DEFAULT_STT_MODEL = "scribe_v2"
DEFAULT_STT_REALTIME_MODEL = "scribe_v2_realtime"
DEFAULT_OUTPUT_DIR = "output"


@dataclass(frozen=True)
class Settings:
    """Runtime settings loaded from environment with sensible defaults."""

    voice_id: str
    tts_model: str
    tts_output_format: str
    stt_model: str
    stt_realtime_model: str
    output_dir: Path

    @property
    def default_speech_path(self) -> Path:
        return self.output_dir / "speech.mp3"


def _env(name: str, default: str) -> str:
    return os.getenv(name, default).strip()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    output_dir = Path(_env("ELEVENLABS_OUTPUT_DIR", DEFAULT_OUTPUT_DIR))
    return Settings(
        voice_id=_env("ELEVENLABS_VOICE_ID", DEFAULT_VOICE_ID),
        tts_model=_env("ELEVENLABS_TTS_MODEL", DEFAULT_TTS_MODEL),
        tts_output_format=_env("ELEVENLABS_TTS_OUTPUT_FORMAT", DEFAULT_TTS_OUTPUT_FORMAT),
        stt_model=_env("ELEVENLABS_STT_MODEL", DEFAULT_STT_MODEL),
        stt_realtime_model=_env("ELEVENLABS_STT_REALTIME_MODEL", DEFAULT_STT_REALTIME_MODEL),
        output_dir=output_dir,
    )
