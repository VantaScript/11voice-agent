"""Streaming TTS and realtime STT — low-latency alternatives to batch agents."""

from __future__ import annotations

import asyncio
import base64
import subprocess
from collections.abc import Callable, Iterator
from pathlib import Path

from elevenlabs.core.api_error import ApiError
from elevenlabs.realtime import AudioFormat, CommitStrategy, RealtimeEvents

from agents.client import get_client
from agents.config import get_settings
from agents.errors import AudioNotFoundError, ValidationError, wrap_api_error

SAMPLE_RATE = 16000
CHUNK_SIZE = 8192
PCM_SUFFIXES = {".pcm", ".s16le", ".raw"}


def stream_text_to_speech(
    text: str,
    *,
    voice_id: str | None = None,
    model_id: str | None = None,
    output_format: str | None = None,
    optimize_streaming_latency: int = 3,
) -> Iterator[bytes]:
    """Yield TTS audio chunks as they arrive (~75ms with flash models)."""
    if not text.strip():
        raise ValidationError("Text cannot be empty.")

    settings = get_settings()
    client = get_client()
    try:
        yield from client.text_to_speech.stream(
            voice_id=voice_id or settings.voice_id,
            text=text,
            model_id=model_id or settings.tts_model,
            output_format=output_format or settings.tts_output_format,
            optimize_streaming_latency=optimize_streaming_latency,
        )
    except ApiError as err:
        raise wrap_api_error(err) from err


def stream_text_to_file(
    text: str,
    *,
    output_path: str | Path | None = None,
    on_chunk: Callable[[int], None] | None = None,
    **kwargs,
) -> Path:
    """Stream TTS to disk, optionally reporting bytes received per chunk."""
    settings = get_settings()
    out = Path(output_path or settings.default_speech_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    with out.open("wb") as f:
        for chunk in stream_text_to_speech(text, **kwargs):
            f.write(chunk)
            if on_chunk:
                on_chunk(len(chunk))

    return out


async def _send_pcm_stream(connection, pcm_path: Path) -> None:
    loop = asyncio.get_event_loop()
    with pcm_path.open("rb") as f:
        while True:
            chunk = await loop.run_in_executor(None, f.read, CHUNK_SIZE)
            if not chunk:
                break
            await connection.send(
                {"audio_base_64": base64.b64encode(chunk).decode("utf-8")}
            )


async def _send_ffmpeg_stream(connection, audio_path: Path) -> None:
    try:
        proc = subprocess.Popen(
            [
                "ffmpeg",
                "-i",
                str(audio_path),
                "-f",
                "s16le",
                "-ar",
                str(SAMPLE_RATE),
                "-ac",
                "1",
                "-",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError as err:
        raise RuntimeError(
            "ffmpeg is required for non-PCM audio. "
            "Install ffmpeg or use PCM: python main.py tts \"...\" "
            "-o output/audio.pcm --format pcm_16000"
        ) from err

    loop = asyncio.get_event_loop()
    try:
        while proc.stdout:
            chunk = await loop.run_in_executor(None, proc.stdout.read, CHUNK_SIZE)
            if not chunk:
                break
            await connection.send(
                {"audio_base_64": base64.b64encode(chunk).decode("utf-8")}
            )
    finally:
        proc.kill()
        proc.wait(timeout=1)


async def realtime_transcribe_file(
    audio_path: str | Path,
    *,
    model_id: str | None = None,
    language_code: str | None = None,
    on_partial: Callable[[str], None] | None = None,
) -> str:
    """
    Transcribe a local audio file via Scribe realtime WebSocket (~150ms latency).

    PCM files (.pcm, .s16le, .raw) are sent directly. Other formats need ffmpeg.
    """
    path = Path(audio_path)
    if not path.is_file():
        raise AudioNotFoundError(f"Audio file not found: {path}")

    settings = get_settings()
    client = get_client()
    committed: list[str] = []
    done = asyncio.Event()

    def on_committed(data: dict) -> None:
        text = data.get("text", "").strip()
        if text:
            committed.append(text)
        done.set()

    def on_partial_event(data: dict) -> None:
        if on_partial:
            on_partial(data.get("text", ""))

    connection = await client.speech_to_text.realtime.connect(
        {
            "model_id": model_id or settings.stt_realtime_model,
            "audio_format": AudioFormat.PCM_16000,
            "sample_rate": SAMPLE_RATE,
            "commit_strategy": CommitStrategy.MANUAL,
            **({"language_code": language_code} if language_code else {}),
        }
    )
    connection.on(RealtimeEvents.COMMITTED_TRANSCRIPT, on_committed)
    if on_partial:
        connection.on(RealtimeEvents.PARTIAL_TRANSCRIPT, on_partial_event)

    try:
        if path.suffix.lower() in PCM_SUFFIXES:
            await _send_pcm_stream(connection, path)
        else:
            await _send_ffmpeg_stream(connection, path)
        await connection.commit()
        await asyncio.wait_for(done.wait(), timeout=30)
    finally:
        await connection.close()

    return " ".join(committed).strip()


def run_realtime_transcribe_file(audio_path: str | Path, **kwargs) -> str:
    """Sync wrapper for realtime_transcribe_file."""
    return asyncio.run(realtime_transcribe_file(audio_path, **kwargs))
