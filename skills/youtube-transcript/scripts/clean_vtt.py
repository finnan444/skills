#!/usr/bin/env python3
"""Clean a WebVTT file (YouTube rolling captions) into plain text paragraphs.

Usage: clean_vtt.py <file.vtt> [--timestamps] [--chapters chapters.json]
                    [--title "Video title"] [--meta "Uploader · 12:34 · <url>"]
Prints one blank-line-separated paragraph per ~30 s block, optionally
prefixed with [MM:SS] and grouped under the video's own chapter headings.
"""
from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path

# A caption cue is ~3 s of speech, far too short to grep or read as prose.
# Blocks close at the first sentence end past MIN_BLOCK_SECONDS so each one
# is self-contained; MAX_BLOCK_SECONDS bounds a speaker who never stops.
MIN_BLOCK_SECONDS = 30
MAX_BLOCK_SECONDS = 60
SENTENCE_END_RE = re.compile(r"[.!?…]['\"»)]?$")

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


def _blocks(segments: list[dict], breaks: list[float]) -> list[dict]:
    """Merge cues into ~30 s paragraphs, breaking on sentence ends.

    `breaks` are start times a paragraph must not run past — chapter
    boundaries, so a paragraph never straddles two topics.
    """
    out: list[dict] = []
    for seg in segments:
        if not out:
            out.append(dict(seg))
            continue
        cur = out[-1]
        span = seg["start"] - cur["start"]
        ended = SENTENCE_END_RE.search(cur["text"])
        crossed = any(cur["start"] < b <= seg["start"] for b in breaks)
        if crossed or span >= MAX_BLOCK_SECONDS or (span >= MIN_BLOCK_SECONDS and ended):
            out.append(dict(seg))
        else:
            cur["text"] = f"{cur['text']} {seg['text']}"
    return out


def load_chapters(path: Path) -> list[dict]:
    """Read yt-dlp's `%(chapters)j` output. `null` means the video has none."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if not data:
        return []
    return [{"start": float(c["start_time"]), "title": c["title"]} for c in data]


def _stamp(start: float) -> str:
    hours, rem = divmod(int(start), 3600)
    minutes, sec = divmod(rem, 60)
    return f"{hours:02d}:{minutes:02d}:{sec:02d}" if hours else f"{minutes:02d}:{sec:02d}"


def format_transcript(
    segments: list[dict], timestamps: bool, chapters: list[dict]
) -> str:
    blocks = _blocks(segments, [c["start"] for c in chapters])
    pending = list(chapters)
    parts: list[str] = []
    for block in blocks:
        while pending and pending[0]["start"] <= block["start"]:
            chapter = pending.pop(0)
            parts.append(f"## [{_stamp(chapter['start'])}] {chapter['title']}")
        parts.append(
            f"[{_stamp(block['start'])}] {block['text']}" if timestamps else block["text"]
        )
    if blocks:
        for chapter in pending:
            parts.append(f"## [{_stamp(chapter['start'])}] {chapter['title']}")
    return "\n\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("vtt", type=Path)
    parser.add_argument(
        "-t", "--timestamps", action="store_true", help="prefix each block with [MM:SS]"
    )
    parser.add_argument(
        "-c", "--chapters", type=Path, help="JSON file from yt-dlp's %%(chapters)j"
    )
    parser.add_argument("--title", help="video title, emitted as an H1 on top")
    parser.add_argument("--meta", help="source line, emitted under the title")
    args = parser.parse_args()
    if not args.vtt.is_file():
        parser.error(f"not a file: {args.vtt}")
    chapters = load_chapters(args.chapters) if args.chapters else []
    text = format_transcript(parse_vtt(args.vtt), args.timestamps, chapters)
    if not text.strip():
        parser.exit(1, "no cues found\n")
    header = [f"# {args.title}"] if args.title else []
    if args.meta:
        header.append(args.meta)
    if header:
        text = "\n\n".join(header + [text])
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
