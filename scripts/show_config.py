"""Step 5 smoke test: print active configuration."""

from agents.config import get_settings


def main() -> None:
    s = get_settings()
    print("ElevenLabs agent settings:")
    print(f"  voice_id:          {s.voice_id}")
    print(f"  tts_model:         {s.tts_model}")
    print(f"  tts_output_format: {s.tts_output_format}")
    print(f"  stt_model:         {s.stt_model}")
    print(f"  output_dir:        {s.output_dir}")
    print(f"  default_speech:    {s.default_speech_path}")


if __name__ == "__main__":
    main()
