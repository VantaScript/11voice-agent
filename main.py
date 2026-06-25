#!/usr/bin/env python3
"""CLI for ElevenLabs STT and TTS agents."""

import argparse
import sys
from pathlib import Path

# Allow `python main.py` without PYTHONPATH=.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from agents.config import get_settings
from agents.stt_agent import speech_to_text
from agents.tts_agent import text_to_speech


def cmd_tts(args: argparse.Namespace) -> int:
    path = text_to_speech(args.text, output_path=args.output)
    print(f"Saved audio to: {path}")
    return 0


def cmd_stt(args: argparse.Namespace) -> int:
    audio = Path(args.audio)
    if not audio.is_file():
        print(f"Error: audio file not found: {audio}", file=sys.stderr)
        return 1

    result = speech_to_text(
        audio,
        language_code=args.language,
        diarize=args.diarize,
        tag_audio_events=args.tag_events,
    )
    if result.language_code and result.language_probability is not None:
        print(f"Language: {result.language_code} ({result.language_probability:.0%})")
    elif result.language_code:
        print(f"Language: {result.language_code}")
    print(result.text)
    return 0


def cmd_config(_: argparse.Namespace) -> int:
    s = get_settings()
    print("ElevenLabs agent settings:")
    print(f"  voice_id:          {s.voice_id}")
    print(f"  tts_model:         {s.tts_model}")
    print(f"  tts_output_format: {s.tts_output_format}")
    print(f"  stt_model:         {s.stt_model}")
    print(f"  output_dir:        {s.output_dir}")
    print(f"  default_speech:    {s.default_speech_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    settings = get_settings()
    parser = argparse.ArgumentParser(
        description="ElevenLabs STT & TTS agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
        '  python main.py tts "Hello world"\n'
        "  python main.py stt output/speech.mp3\n"
        "  python main.py config",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    tts = sub.add_parser("tts", help="Convert text to speech")
    tts.add_argument("text", help="Text to speak")
    tts.add_argument(
        "-o",
        "--output",
        type=Path,
        default=settings.default_speech_path,
        help=f"Output MP3 path (default: {settings.default_speech_path})",
    )
    tts.set_defaults(func=cmd_tts)

    stt = sub.add_parser("stt", help="Transcribe audio to text")
    stt.add_argument("audio", help="Path to audio file (MP3, WAV, etc.)")
    stt.add_argument(
        "-l",
        "--language",
        help="Language hint, e.g. eng or en (auto-detect if omitted)",
    )
    stt.add_argument(
        "--diarize",
        action="store_true",
        help="Label speakers in the transcript",
    )
    stt.add_argument(
        "--tag-events",
        action="store_true",
        help="Tag audio events like (laughter)",
    )
    stt.set_defaults(func=cmd_stt)

    config = sub.add_parser("config", help="Show active settings")
    config.set_defaults(func=cmd_config)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
