"""Step 4 smoke test: transcribe audio to text."""

import sys
from pathlib import Path

from agents.stt_agent import speech_to_text


def main() -> None:
    audio = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("output/test_tts.mp3")
    if not audio.is_file():
        print(f"Audio file not found: {audio}")
        print("Run Step 3 first: PYTHONPATH=. python scripts/test_tts.py")
        sys.exit(1)

    result = speech_to_text(audio)
    print(f"Audio: {audio}")
    print(f"Language: {result.language_code} ({result.language_probability:.0%})"
          if result.language_code and result.language_probability is not None
          else f"Language: {result.language_code or 'auto-detected'}")
    print(f"Transcript: {result.text}")


if __name__ == "__main__":
    main()
