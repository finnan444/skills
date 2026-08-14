---
name: youtube-transcript
description: Pull a YouTube transcript (captions only, no video download). Use when the user pastes a YouTube URL, youtu.be link, Shorts URL, or 11-char video ID and wants the transcript, subtitles, captions, or a text dump of what was said. Also use for /youtube-transcript.
---

# YouTube transcript

Captions only. Never download the video.

`scripts/clean_vtt.py` sits next to this file. Set `SKILL_DIR` to the absolute directory of the SKILL.md you Read, then call `"$SKILL_DIR/scripts/clean_vtt.py"`.

## Process

1. **Source.** Accept `youtube.com/watch?v=`, `youtu.be/`, `youtube.com/shorts/`, `youtube.com/embed/`, `youtube.com/live/`, or a raw 11-char id `[A-Za-z0-9_-]{11}`. Normalize to `https://www.youtube.com/watch?v=<id>`. Anything else: stop. Done when you have that watch URL and the 11-char id.

2. **Preflight.** Run `yt-dlp --version`. Missing → tell the user `brew install yt-dlp` (or their OS equivalent) and stop. Done when yt-dlp prints a version.

3. **Metadata + manual captions.** In a fresh temp dir (`mktemp -d /tmp/youtube-transcript-XXXXXX`):

   ```bash
   yt-dlp --skip-download \
     --print "%(id)s" --print "%(title)s" --print "%(uploader)s" --print "%(duration_string)s" --print "%(is_live)s" --print "%(was_live)s" \
     --write-subs --sub-format vtt --sub-langs ".*-orig,ru,en" \
     -o "<tmpdir>/%(id)s" \
     "https://www.youtube.com/watch?v=<id>"
   ```

   `--sub-langs` takes regexes, not globs — `.*-orig` is valid, `*-orig` errors out. Keep it to these three: a broad pattern like `en.*` also matches machine-translated tracks (`en-de-DE`, `en-ja`, …), which means a download per track and an HTTP 429. Listing `.*-orig` first also makes yt-dlp fetch the preferred track first. Done when you have title, uploader, duration, `is_live`, `was_live`, and know whether any `.vtt` landed.

4. **Auto captions, only if step 3 produced no `.vtt`.** Same command with `--write-auto-subs` added. If that also produces nothing, retry once with `--sub-langs "all,-live_chat"`. Still none → report that this video has no captions and stop.

   `is_live` is `True` → skip the retry and stop right there: YouTube only generates auto captions once the broadcast ends and the recording is processed, so a stream in progress offers nothing but a `live_chat` track. Tell the user the stream is still live and the transcript will be available a few hours after it ends.

   `is_live` is `False` but `was_live` is `True` → run the retry as usual, but if it finds nothing, say the recording is still being processed rather than that the video has no captions, and suggest retrying in a few hours. A just-ended stream looks like a normal video — real duration, no `live_chat` track — hours before its captions appear.

   The pass that produced the file is the only reliable source of the manual/auto label — yt-dlp names both `<id>.<lang>.vtt` with no `.auto.` marker. Done when at least one `.vtt` exists and you know which pass wrote it.

   `HTTP Error 429: Too Many Requests` on a track is harmless as long as a preferred track already landed — go on to step 5. If 429 kills every track, wait ~60 s and rerun the same command once with `--sleep-subtitles 3`.

5. **Pick the track.** Prefer a `<lang>-orig` file, whatever that language is — the suffix marks the video's original language, and every other track in an auto-caption set is a machine translation of it, so it compounds the recognizer's errors. On an English Short, `en-orig` gives `Why does no one in America use bidet?` while `ru` gives «никто не использует **постель** для мытья задницы». If no `-orig` file (manual captions never carry the suffix), prefer `ru`, then `en`, then any other language. Ignore `live_chat`. Done when one VTT path is chosen.

6. **Clean.**

   ```bash
   "$SKILL_DIR/scripts/clean_vtt.py" "<vtt>" > "<tmpdir>/transcript.txt"
   ```

   Non-zero exit → report and stop. Done when `transcript.txt` is non-empty.

7. **Report.** In chat, in this order:

   - one line: `<title> · <uploader> · <duration> · <lang> · manual|auto`. A live or just-ended video has no duration — yt-dlp prints `NA`; write `live` instead.
   - path to `transcript.txt`
   - a short summary of what the video covers

   Paste the transcript body into chat only if the user asked for the raw text, or if it is under ~200 lines. Otherwise the file on disk is the deliverable — a long transcript buries the rest of the conversation.

   If the video was unavailable, private, or yt-dlp asked to sign in: say that and stop. Do not retry with cookies unless the user asks.
