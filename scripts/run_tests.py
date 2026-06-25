#!/usr/bin/env python3
"""Step 9 — integration tests for STT, TTS, pipeline, and error handling."""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from agents.client import get_client
from agents.config import get_settings
from agents.errors import AudioNotFoundError, ValidationError
from agents.pipeline import roundtrip
from agents.stt_agent import speech_to_text
from agents.tts_agent import text_to_speech


@dataclass
class TestResult:
    name: str
    passed: bool
    detail: str = ""


def _run(name: str, fn) -> TestResult:
    try:
        fn()
        return TestResult(name, True)
    except Exception as err:
        return TestResult(name, False, str(err))


def _run_cli(args: list[str], *, expect_code: int) -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "main.py"), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != expect_code:
        msg = result.stderr.strip() or result.stdout.strip() or "no output"
        raise AssertionError(f"expected exit {expect_code}, got {result.returncode}: {msg}")


def test_config() -> None:
    settings = get_settings()
    assert settings.voice_id
    assert settings.tts_model
    assert settings.stt_model


def test_client() -> None:
    client = get_client()
    assert client.text_to_speech is not None
    assert client.speech_to_text is not None


def test_tts() -> None:
    path = text_to_speech("Step nine test.", output_path=ROOT / "output" / "test_step9.mp3")
    assert path.is_file()
    assert path.stat().st_size > 1000


def test_stt() -> None:
    audio = ROOT / "output" / "test_step9.mp3"
    result = speech_to_text(audio)
    assert result.text.strip()
    assert len(result.text) > 3


def test_roundtrip() -> None:
    result = roundtrip(
        "Roundtrip test",
        output_path=ROOT / "output" / "test_step9_roundtrip.mp3",
    )
    assert result.audio_path.is_file()
    assert result.transcript.strip()


def test_validation_error() -> None:
    try:
        text_to_speech("   ")
        raise AssertionError("expected ValidationError")
    except ValidationError:
        pass


def test_missing_audio() -> None:
    try:
        speech_to_text(ROOT / "output" / "does_not_exist.mp3")
        raise AssertionError("expected AudioNotFoundError")
    except AudioNotFoundError:
        pass


def test_cli_validation() -> None:
    _run_cli(["tts", "   "], expect_code=2)


def test_cli_missing_file() -> None:
    _run_cli(["stt", "missing_file.mp3"], expect_code=1)


TESTS = [
    ("config loads", test_config),
    ("client initializes", test_client),
    ("TTS generates audio", test_tts),
    ("STT transcribes audio", test_stt),
    ("roundtrip pipeline", test_roundtrip),
    ("validation error (agent)", test_validation_error),
    ("missing file (agent)", test_missing_audio),
    ("validation error (CLI)", test_cli_validation),
    ("missing file (CLI)", test_cli_missing_file),
]


def run_all() -> int:
    print("Running ElevenLabs agent tests...\n")
    results: list[TestResult] = []

    for name, fn in TESTS:
        result = _run(name, fn)
        results.append(result)
        status = "PASS" if result.passed else "FAIL"
        line = f"  [{status}] {name}"
        if result.detail:
            line += f" — {result.detail}"
        print(line)

    passed = sum(1 for r in results if r.passed)
    total = len(results)
    print(f"\n{passed}/{total} tests passed")

    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(run_all())
