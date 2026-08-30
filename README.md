# Agent Skills

Three reusable workflows for Claude Code, Codex, and Grok Build: reliable Panda CSS changes, TRIZ problem analysis, and readable YouTube transcripts. Instead of making you repeat a long prompt, each skill defines the checks, failure paths, and done conditions the agent should follow.

- **Cross-agent.** The same `SKILL.md` directories work in Claude Code, Codex, and Grok Build—no separate forks to maintain.
- **Process, not prose.** Each skill says what to inspect, what to do, and how to know the work is complete.
- **Explicit when appropriate.** `triz` and `youtube-transcript` run only when you name them; `panda-css` can activate automatically for Panda tasks.
- **Gotchas included.** The procedures cover Panda CSS extraction gaps, unavailable caption tracks, and solution bias in problem statements.
- **Untrusted input stays data.** The transcript workflow never treats video titles, captions, or fetched material as instructions.

```text
# Claude Code or Grok Build
/youtube-transcript https://youtu.be/<id>
# Codex
$youtube-transcript https://youtu.be/<id>
# → <video-title-slug>.md
# → <video-title-slug>.map.md for longer videos
```

---

## Contents

- [Available skills](#available-skills)
- [Compatibility](#compatibility)
- [Installation](#installation)
- [Usage](#usage)
- [YouTube transcript output](#youtube-transcript-output)
- [Contributing](#contributing)
- [License](#license)

## Available skills

<!-- SKILLS:START -->
| Skill | What it helps with | Activation |
|-------|--------------------|------------|
| [panda-css](skills/panda-css/) | Build and review Panda CSS styles while respecting the target project's config, generated APIs, tokens, and static extraction rules. | Automatic for Panda CSS tasks, or explicit. |
| [triz](skills/triz/) | Reframe a problem without its assumed solution, expose the contradiction, and turn existing system resources into testable directions. | Explicit only. |
| [youtube-transcript](skills/youtube-transcript/) | Fetch existing YouTube captions without downloading video, clean them into readable prose, and map longer transcripts for cheap follow-up questions. | Explicit only. |
<!-- SKILLS:END -->

## Compatibility

The skills use the open Agent Skills directory format: a required `SKILL.md` plus optional scripts, references, and host metadata.

| Host | Explicit invocation | Project skill directory |
|------|---------------------|-------------------------|
| Claude Code | `/skill-name` | `.claude/skills/` |
| Codex | `$skill-name` or `/skills` | `.agents/skills/` |
| Grok Build | `/skill-name` | `.grok/skills/` |

- [Codex supports](https://developers.openai.com/codex/skills) `SKILL.md`, scripts, references, and `agents/openai.yaml` metadata.
- [Grok Build supports](https://docs.x.ai/build/features/skills-plugins-marketplaces) native `.grok/skills/` directories and Claude Code compatibility paths.
- The [`skills` CLI](https://github.com/vercel-labs/skills) can install this repository for all three hosts.

> **Grok on the web and mobile is different from Grok Build.** The installation commands below target local coding agents. In particular, do not assume `youtube-transcript` works in hosted Grok: its workflow requires local `yt-dlp` and Python.

---

## Installation

### Install with the Skills CLI

The CLI puts each skill in the directory expected by the selected agent:

```bash
# See the available skills
npx skills add finnan444/skills --list

# Install every skill for all three supported agents
npx skills add finnan444/skills --skill '*' \
  -a claude-code -a codex -a grok

# Or install one skill for one agent
npx skills add finnan444/skills --skill panda-css -a codex
```

Use `-g` with an install command to make the skills available across projects. Without it, the CLI installs them into the current project.

### Install manually

Clone the repository, then copy the skill directories into the folder for your agent:

```bash
git clone https://github.com/finnan444/skills.git /tmp/finnan444-skills

# Claude Code
mkdir -p .claude/skills
cp -R /tmp/finnan444-skills/skills/{panda-css,triz,youtube-transcript} .claude/skills/

# Codex
mkdir -p .agents/skills
cp -R /tmp/finnan444-skills/skills/{panda-css,triz,youtube-transcript} .agents/skills/

# Grok Build
mkdir -p .grok/skills
cp -R /tmp/finnan444-skills/skills/{panda-css,triz,youtube-transcript} .grok/skills/
```

### YouTube transcript prerequisites

Installing the other skills adds no prerequisites of its own. `youtube-transcript` requires `yt-dlp` and Python 3:

```bash
brew install yt-dlp   # or use your operating system's package manager
python3 --version
```

If you use the self-contained `yt-dlp_macos` binary, install Python separately. On macOS, `/usr/bin/python3` may be an Xcode Command Line Tools stub; `xcode-select --install` makes it usable.

---

## Usage

### Panda CSS

Start a Panda CSS task normally—for example, “add a `size` variant to this recipe.” The skill activates automatically, reads the package's Panda config and conventions first, and checks that generated CSS can be statically extracted.

### TRIZ

Invoke the skill with a problem statement that may already contain an assumed solution:

```text
# Claude Code or Grok Build
/triz Add a Redis cache because the orders page takes eight seconds to load.

# Codex
$triz Add a Redis cache because the orders page takes eight seconds to load.
```

The result separates verified facts from hypotheses, states the contradiction, proposes one to three directions using resources already in the system, and ends with a measurable experiment. The skill and its worked examples are written in Russian.

### YouTube transcript

Invoke the skill with a supported YouTube URL or an 11-character video ID:

```text
# Claude Code or Grok Build
/youtube-transcript https://www.youtube.com/watch?v=<id>

# Codex
$youtube-transcript https://www.youtube.com/watch?v=<id>
```

It accepts `watch?v=`, `youtu.be/`, `/shorts/`, `/embed/`, and `/live/` URLs. It uses existing manual or automatic captions and never downloads the video.

## YouTube transcript output

The transcript is saved as `<video-title-slug>.md`, with the video's title and source at the top. Captions become readable paragraphs of roughly 30–60 seconds and follow the uploader's chapter boundaries when available:

```markdown
# <video title>

<uploader> · <duration> · https://www.youtube.com/watch?v=<id>

## [00:00] <first chapter title>

[00:00] <spoken text, grouped into a readable paragraph>
```

Videos with 25 or more transcript paragraphs also get `<video-title-slug>.map.md`: a short abstract, an index of 8–20 timestamped topics when uploader chapters are unavailable, and notable claims worth finding again. Follow-up questions can use that map and read only the relevant transcript section:

```bash
awk '/^\[04:12\]/,/^\[09:30\]/' <video-title-slug>.md
```

The entire fetch, cleanup, and map generation runs in one subagent so the main conversation receives the compact report instead of the full transcript.

---

## Contributing

Found a missing edge case or have a skill to suggest? Issues and pull requests are welcome.

## License

[MIT](LICENSE) — use these skills however you want.
