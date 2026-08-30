# Skills for Claude Code

Skills that teach [Claude Code](https://claude.com/claude-code) how to do a specific job the way it should be done — Panda CSS styling, YouTube transcripts — so you stop re-explaining the same rules and gotchas in every session. Each one is a short, numbered procedure with exact commands and explicit done-conditions, not a pile of advice.

- **Process, not prose.** Every skill is a numbered checklist: what to run, what "done" means for each step, and what to do when a step fails.
- **Gotchas already paid for.** The traps are written down — `yt-dlp --print` silently implying `--simulate`, `--sub-langs` taking regexes and not globs, HTTP 429 on caption tracks, Panda emitting class names with no CSS when a value isn't statically analyzable.
- **Injection-hardened.** Skills that read third-party content (video captions, uploader titles, fetched docs) treat it as data, never as instructions.
- **No dependencies to install.** Plain Markdown plus one Python script, no runtime, no config.

## Available skills

<!-- SKILLS:START -->
| Skill | Description |
|-------|-------------|
| [panda-css](skills/panda-css/) | Build styles with Panda CSS. Use when creating, editing, or reviewing any code that uses Panda CSS — css(), cva(), sva(), recipes, patterns, tokens, semantic tokens, panda.config, theming, codegen, or JSX styled components. Also use when Panda emits class names but no CSS. Supports React, Vue, Svelte, Solid, and any framework with PostCSS. |
| [youtube-transcript](skills/youtube-transcript/) | Pull a YouTube transcript from existing captions via yt-dlp (captions only; prefers original-language track, then ru, then en). Fetches, cleans and maps the video in a subagent. |
<!-- SKILLS:END -->

---

## Example

Ask for a transcript in Claude Code:

```
/youtube-transcript https://youtu.be/<id>
```

You get `<video-title-slug>.md` — headed by the video's own title and source line, with ~30-second paragraphs grouped under the uploader's chapter marks:

```markdown
# <video title>

<uploader> · <duration> · https://www.youtube.com/watch?v=<id>

## [00:00] <first chapter title>

[00:00] <spoken text, broken at sentence ends into readable paragraphs>
```

Anything past ~12 minutes also gets `<video-title-slug>.map.md`: an abstract, a
timestamped index of 8-20 topics, and the claims worth finding again. The map is
what your follow-up questions and detailed write-ups read — it is a couple of
thousand tokens against a transcript that can be forty, and its timestamps are
exact, so one section comes back with

```bash
awk '/^\[04:12\]/,/^\[09:30\]/' <video-title-slug>.md
```

No video is downloaded. The whole fetch — yt-dlp, cleaning, the full read the map
and the summary need — happens in a subagent, so your main conversation only ever
sees the report.

---

## Installation

### Option 1: CLI install (recommended)

[`npx skills`](https://github.com/vercel-labs/skills) copies the skills into `.claude/skills/` for you:

```bash
# All skills, into the current project
npx skills add finnan444/skills

# Just one
npx skills add finnan444/skills --skill panda-css

# See what's available first
npx skills add finnan444/skills --list
```

### Option 2: Manual

Copy the skill directory into your project (or `~/.claude/skills/` to have it everywhere):

```bash
git clone https://github.com/finnan444/skills.git /tmp/finnan444-skills
mkdir -p .claude/skills
cp -R /tmp/finnan444-skills/skills/youtube-transcript .claude/skills/
```

Then restart Claude Code (or run `/doctor`) so it picks up the new skill.

### Prerequisites

Only `youtube-transcript` needs anything extra:

```bash
brew install yt-dlp   # or your OS equivalent
python3 --version     # 3.x, for the caption cleaner
```

yt-dlp is itself a Python program, so installing it through Homebrew or pip brings
an interpreter along. The gap is the self-contained `yt-dlp_macos` binary, which
keeps its Python inside the bundle: there, install `python3` separately. On macOS
`/usr/bin/python3` is an Xcode Command Line Tools stub — `xcode-select --install`
turns it into a real interpreter.

## Usage

- **panda-css** is picked up automatically — start editing Panda code and ask for what you want ("add a `size` variant to this recipe"). The skill loads itself when the task touches Panda.
- **youtube-transcript** is slash-command only (`disable-model-invocation: true`), so it never fires on its own. Invoke it with `/youtube-transcript <url>`; it accepts `watch?v=`, `youtu.be/`, `/shorts/`, `/embed/`, `/live/`, or a bare 11-character video id.

## Contributing

Found a way to improve a skill? Have a new skill to suggest? PRs and issues welcome.

## License

[MIT](LICENSE) — use these however you want.
