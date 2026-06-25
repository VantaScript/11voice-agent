"""Step 3 smoke test: generate speech from text."""

import sys

from agents.tts_agent import text_to_speech


def main() -> None:
    text = sys.argv[1] if len(sys.argv) > 1 else "Hello! This is the ElevenLabs TTS agent."
    path = text_to_speech(text, output_path="output/test_tts.mp3")
    print(f"Saved audio to: {path}")
    print(f"Text: {text}")


if __name__ == "__main__":
    main()
