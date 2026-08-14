#!/usr/bin/env python3
"""Clean a WebVTT file (YouTube rolling captions) into timestamped plain text.

Usage: clean_vtt.py <file.vtt>
Prints one line per cue: [MM:SS] text
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

TS_RE = re.compile(
    r"(\d{2}):(\d{2}):(\d{2})[.,](\d{3})\s+-->\s+(\d{2}):(\d{2}):(\d{2})[.,](\d{3})"
)
TAG_RE = re.compile(r"<[^>]+>")


def _to_seconds(h: str, m: str, s: str, ms: str) -> float:
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def _cue_lines(lines: list[str], i: int) -> tuple[list[str], int]:
    """Collect the text lines of one cue, stripped of inline tags.

    Runs to the next timestamp line rather than to the next blank line:
    YouTube pads cues with whitespace-only lines, which a blank-line
    terminator would mistake for the end of the cue.
    """
    out: list[str] = []
    while i < len(lines) and not TS_RE.match(lines[i].strip()):
        cleaned = html.unescape(TAG_RE.sub("", lines[i])).strip()
        if cleaned:
            out.append(cleaned)
        i += 1
    return out, i


def parse_vtt(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    segments: list[dict] = []
    prev_lines: list[str] = []
    i = 0
    while i < len(lines):
        match = TS_RE.match(lines[i].strip())
        if not match:
            i += 1
            continue
        start = _to_seconds(*match.groups()[:4])
        cur_lines, i = _cue_lines(lines, i + 1)
        # YouTube rolling captions repeat the tail of the previous cue as the
        # leading lines of the next one. Strip that carry-over.
        new_lines = list(cur_lines)
        while new_lines and new_lines[0] in prev_lines:
            new_lines.pop(0)
        prev_lines = cur_lines
        cue_text = " ".join(new_lines).strip()
        if cue_text:
            segments.append({"start": start, "text": cue_text})
    return _dedupe(segments)


def _dedupe(segments: list[dict]) -> list[dict]:
    out: list[dict] = []
    for seg in segments:
        if out and seg["text"] == out[-1]["text"]:
            continue
        if out and seg["text"].startswith(out[-1]["text"] + " "):
            out[-1]["text"] = seg["text"]
            continue
        out.append(seg)
    return out


def format_transcript(segments: list[dict]) -> str:
    lines = []
    for seg in segments:
        total = int(seg["start"])
        hours, rem = divmod(total, 3600)
        minutes, sec = divmod(rem, 60)
        stamp = f"{hours:02d}:{minutes:02d}:{sec:02d}" if hours else f"{minutes:02d}:{sec:02d}"
        lines.append(f"[{stamp}] {seg['text']}")
    return "\n".join(lines)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: clean_vtt.py <file.vtt>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"not a file: {path}", file=sys.stderr)
        return 2
    text = format_transcript(parse_vtt(path))
    if not text.strip():
        print("no cues found", file=sys.stderr)
        return 1
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
