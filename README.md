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
| 9 | Test the agents ✅ |
| 10 | Streaming & realtime ✅ |

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
python main.py test
```

## Streaming & realtime (Step 10)

| Mode | Command | Model | Latency |
|------|---------|-------|---------|
| Batch TTS | `python main.py tts "..."` | `eleven_flash_v2_5` | ~1s |
| **Stream TTS** | `python main.py stream-tts "..."` | same | **~75ms** first chunk |
| Batch STT | `python main.py stt audio.mp3` | `scribe_v2` | ~1s |
| **Realtime STT** | `python main.py stream-stt audio.mp3 --partials` | `scribe_v2_realtime` | **~150ms** |

Realtime STT requires [ffmpeg](https://ffmpeg.org/download.html) for MP3/WAV, or use PCM directly:

```bash
python main.py tts "Hello" -o output/audio.pcm --format pcm_16000
python main.py stream-stt output/audio.pcm --partials
```

### Further reading

- [ElevenLabs docs](https://elevenlabs.io/docs/overview/intro) — models, voices, credits
- [Speech Engine](https://elevenlabs.io/docs/overview/capabilities/speech-engine) — voice agents with your own LLM over WebSocket
- [ElevenAgents](https://elevenlabs.io/docs/eleven-agents) — no-code conversational agent builder
