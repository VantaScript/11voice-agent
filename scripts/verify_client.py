"""Step 2 smoke test: confirm the shared client loads and initializes."""

from agents.client import get_client


def main() -> None:
    client = get_client()
    print("ElevenLabs client ready.")
    print(f"  TTS: client.text_to_speech")
    print(f"  STT: client.speech_to_text")
    print(f"  Type: {type(client).__name__}")


if __name__ == "__main__":
    main()
