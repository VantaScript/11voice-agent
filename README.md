# ElevenLabs STT & TTS Agents

Step-by-step agents using [ElevenLabs API](https://elevenlabs.io/docs/overview/intro).

| Step | Topic |
|------|-------|
| 1 | Project setup & API key |
| 2 | Shared ElevenLabs client ✅ |
| 3 | TTS agent (text → speech) ✅ |
| 4 | STT agent (speech → text) ✅ |
| 5 | Config & defaults ✅ |
| 6 | CLI entry point ✅ |
| 7 | End-to-end pipeline (TTS → STT round-trip) ✅ |
| 8 | Error handling ✅ |
| 9 | Test the agents |
| 10 | Next steps (streaming, realtime) |

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your key
PYTHONPATH=. python scripts/verify_client.py
PYTHONPATH=. python scripts/show_config.py
python main.py config
python main.py tts "Hello from ElevenLabs"
python main.py stt output/speech.mp3
python main.py roundtrip "Test round-trip transcription"
```
