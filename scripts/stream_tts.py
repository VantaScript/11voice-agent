"""Step 10 demo — stream TTS chunks to a file with progress."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from agents.streaming import stream_text_to_file


def main() -> None:
    text = sys.argv[1] if len(sys.argv) > 1 else "Streaming text to speech in real time."
    total = 0

    def on_chunk(size: int) -> None:
        nonlocal total
        total += size
        print(f"\r  received {total:,} bytes", end="", flush=True)

    path = stream_text_to_file(
        text,
        output_path=ROOT / "output" / "stream_tts.mp3",
        on_chunk=on_chunk,
    )
    print(f"\nSaved to: {path}")


if __name__ == "__main__":
    main()
