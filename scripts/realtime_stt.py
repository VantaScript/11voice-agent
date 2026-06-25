"""Step 10 demo — realtime STT via WebSocket (~150ms latency)."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from agents.streaming import run_realtime_transcribe_file


def main() -> None:
    audio = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "output" / "speech.mp3"
    if not audio.is_file():
        print(f"Audio not found: {audio}")
        print('Run: python main.py tts "Hello" first')
        sys.exit(1)

    print(f"Realtime transcribing: {audio}")
    print("Partials:", end=" ", flush=True)

    def on_partial(text: str) -> None:
        if text:
            print(f"\r  partial: {text}", end="", flush=True)

    transcript = run_realtime_transcribe_file(audio, on_partial=on_partial)
    print(f"\nFinal: {transcript}")


if __name__ == "__main__":
    main()
