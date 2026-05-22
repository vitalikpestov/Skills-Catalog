# ffmpeg-skill

> **Edit videos from your terminal with natural language.** Cut, merge, compress, subtitle, GIF, watermark, speed, stabilize — just describe what you want.

---

Stop memorizing ffmpeg flags. Just say:

```
"cut the first 30 seconds of this video"
"merge these 3 clips into one"
"extract the audio as mp3"
"make a GIF from 0:15 to 0:20"
"compress this video to under 10MB"
"add subtitles from this SRT file"
"add a watermark in the bottom-right corner"
"slow motion at 0.5x"
"add 2-second fade in and fade out"
```

Claude Code translates your intent into the right ffmpeg command — or chains multiple commands for complex edits.

## What You Get

**18 high-level commands** that cover 90% of video editing tasks, plus raw ffmpeg access for the other 10%.

| Command | What it does |
|---------|-------------|
| `info` | Duration, resolution, codecs, file size, bitrate |
| `cut` | Extract a segment by start/end time or duration |
| `merge` | Concatenate multiple videos (stream copy or re-encode) |
| `extract-audio` | Rip audio as MP3, AAC, Opus, WAV, FLAC, OGG |
| `subtitles` | Burn SRT subtitles into the video |
| `resize` | Change resolution (auto-scale with -1) |
| `gif` | High-quality two-pass GIF creation |
| `thumbnail` | Extract a single frame as JPG/PNG |
| `thumbnails` | Extract N evenly-spaced frames |
| `compress` | Reduce file size with CRF quality control |
| `speed` | Speed up or slow down (audio pitch preserved) |
| `watermark` | Add image overlay at any corner or center |
| `text` | Burn text with font size, color, position, timing |
| `convert` | Change container/codec (MP4, WebM, MKV, MOV) |
| `frames` | Extract all frames or every Nth frame |
| `audio-replace` | Swap the audio track |
| `volume` | Adjust audio level (multiplier or dB) |
| `fade` | Add fade in/out (video + audio synced) |
| `stabilize` | Fix shaky footage (two-pass vidstab) |

All commands output JSON for easy parsing and chaining.

## Quick Start

### 1. Prerequisites

- **ffmpeg** installed and on PATH
- **Python 3.8+**
- **Claude Code**

```bash
# Check ffmpeg
ffmpeg -version

# On Ubuntu/Debian
sudo apt install ffmpeg

# On macOS
brew install ffmpeg

# On Windows
# Download from https://ffmpeg.org/download.html
```

### 2. Install

```bash
mkdir -p ~/.claude/commands

# Download the skill
curl -o ~/.claude/commands/ffmpeg.md \
  https://raw.githubusercontent.com/MastroMimmo/ffmpeg-skill/main/ffmpeg.md

# Clone the CLI tool
git clone https://github.com/MastroMimmo/ffmpeg-skill.git ~/ffmpeg-skill
```

Update the script path in `~/.claude/commands/ffmpeg.md`:
```
SCRIPT="~/ffmpeg-skill/scripts/fftools.py"
```

### 3. Use

Just talk naturally in Claude Code:

```
"show me the info for video.mp4"
"trim from 1:30 to 2:45 and save as clip.mp4"
"make a 3-second GIF from the best part"
"compress this 2GB file, I need it under 100MB"
"replace the audio with this soundtrack.mp3"
```

## Examples

### Get video info
```bash
python3 fftools.py info input.mp4
```
```json
{
  "file": "input.mp4",
  "streams": [
    {"type": "video", "codec": "h264", "width": 1920, "height": 1080, "fps": 30.0},
    {"type": "audio", "codec": "aac", "sample_rate": "44100", "channels": 2}
  ],
  "format": {
    "duration": 125.5,
    "duration_human": "02:05.50",
    "size_human": "45.2 MB",
    "bit_rate": 2880000
  }
}
```

### Cut + Compress + GIF pipeline
```bash
# 1. Extract the best 10 seconds
python3 fftools.py cut input.mp4 clip.mp4 --start 00:01:15 --duration 10

# 2. Compress for sharing
python3 fftools.py compress clip.mp4 clip_small.mp4 --crf 28

# 3. Make a preview GIF
python3 fftools.py gif clip.mp4 preview.gif --fps 12 --width 400
```

### Add subtitles + watermark
```bash
# Burn subtitles
python3 fftools.py subtitles input.mp4 subbed.mp4 --srt captions.srt

# Add logo watermark
python3 fftools.py watermark subbed.mp4 final.mp4 --watermark logo.png --position bottom-right
```

### Slow motion + fade
```bash
python3 fftools.py speed input.mp4 slowmo.mp4 --factor 0.5
python3 fftools.py fade slowmo.mp4 final.mp4 --fade-in 2 --fade-out 3
```

## Advanced: Raw ffmpeg

The skill also teaches Claude Code raw ffmpeg for complex operations:

- **Picture-in-picture** — Overlay a small video on a large one
- **Side-by-side comparison** — Stack two videos horizontally
- **Grid/mosaic** — 2x2 or 3x3 video grids
- **Green screen removal** — Chroma key compositing
- **Crossfade transitions** — Smooth transitions between clips
- **Color correction** — Brightness, contrast, saturation
- **Noise reduction** — Audio denoising with FFT
- **Timelapse** — Image sequence to video
- **Video from image + audio** — Static image with audio track

## CRF Quality Guide

| CRF | Quality | File size | Best for |
|-----|---------|-----------|----------|
| 18 | Visually lossless | Large | Archival |
| 23 | High | Medium | Default |
| 28 | Good | Small | Sharing |
| 32 | Acceptable | Very small | Social media |

Each +6 roughly halves the file size.

## Why a Helper Script?

FFmpeg is incredibly powerful but has a brutal CLI interface. The `fftools.py` wrapper:

1. **Simplifies flags** — `--start`, `--end` instead of `-ss`, `-to` placement order gotchas
2. **JSON output** — Every command returns structured JSON, not wall-of-text logs
3. **Two-pass GIFs** — Automatic palette generation for high-quality GIFs
4. **Smart codec selection** — Picks the right codec based on output extension
5. **Size reporting** — Compression shows original vs. compressed with % reduction
6. **Zero dependencies** — Python standard library only

But you're never locked in — the skill also teaches Claude raw ffmpeg for anything the wrapper doesn't cover.

## Project Structure

```
ffmpeg-skill/
├── ffmpeg.md              # Skill file (copy to ~/.claude/commands/)
├── scripts/
│   └── fftools.py         # CLI wrapper — Python stdlib, zero deps
└── README.md
```

## License

MIT — see [LICENSE](LICENSE).
