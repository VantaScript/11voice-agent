"""Shared ElevenLabs API client used by STT and TTS agents."""

import os
from functools import lru_cache

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

from agents.errors import ConfigError

load_dotenv()

ENV_API_KEY = "ELEVENLABS_API_KEY"


def _load_api_key() -> str:
    api_key = os.getenv(ENV_API_KEY)
    if not api_key:
        raise ConfigError(
            f"Missing {ENV_API_KEY}. Copy .env.example to .env and add your key."
        )
    return api_key


@lru_cache(maxsize=1)
def get_client() -> ElevenLabs:
    """Return a cached ElevenLabs client (one instance per process)."""
    return ElevenLabs(api_key=_load_api_key())
