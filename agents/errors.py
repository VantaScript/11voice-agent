"""Errors and user-friendly messages for STT/TTS agents."""

from __future__ import annotations

from typing import Any

from elevenlabs.core.api_error import ApiError


class AgentError(Exception):
    """Base exception for agent failures."""


class ConfigError(AgentError):
    """Missing or invalid configuration (e.g. API key)."""


class ValidationError(AgentError):
    """Invalid user input."""


class AudioNotFoundError(AgentError):
    """Audio file path does not exist."""


class ElevenLabsApiError(AgentError):
    """ElevenLabs API returned an error."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        body: Any = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.body = body


def api_error_message(err: ApiError) -> str:
    """Extract a readable message from an ElevenLabs ApiError."""
    body = err.body
    if isinstance(body, dict):
        detail = body.get("detail")
        if isinstance(detail, dict):
            msg = detail.get("message")
            if msg:
                return str(msg)
            status = detail.get("status")
            if status:
                return f"API error: {status}"
        if isinstance(detail, str):
            return detail
    if err.status_code == 401:
        return "Invalid or unauthorized API key. Check ELEVENLABS_API_KEY in .env"
    if err.status_code == 429:
        return "Rate limit exceeded. Wait a moment and try again."
    if err.status_code == 402:
        return "Insufficient credits. Check your ElevenLabs account balance."
    return f"ElevenLabs API error (HTTP {err.status_code})"


def wrap_api_error(err: ApiError) -> ElevenLabsApiError:
    return ElevenLabsApiError(
        api_error_message(err),
        status_code=err.status_code,
        body=err.body,
    )
