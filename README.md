# Frontend Skills for Claude Code

A collection of frontend skills designed to enhance the capabilities of Claude Code, an AI assistant for developers. These skills cover a wide range of frontend technologies and best practices, enabling Claude Code to assist with various aspects of frontend development.

## What are Skills?

Skills are markdown files that give AI agents specialized knowledge and workflows for specific tasks. When you add these to your project, Claude Code can recognize when you're working on a marketing task and apply the right frameworks and best practices.

## Available Skills

<!-- SKILLS:START -->
| Skill | Description |
|-------|-------------|
| [skeleton-dev](skills/skeleton-dev/) | Build UI with Skeleton UI v4 (any framework). Use when creating, editing, or reviewing any component that uses Skeleton UI — buttons, modals, tabs, navigation, forms, cards, avatars, etc. Also use when questions involve Skeleton presets, color pairings, composed component patterns, or theming. Supports Svelte, React, and framework-agnostic usage. |
<!-- SKILLS:END -->

## Installation

### Option 1: CLI Install (Recommended)

Use [npx skills](https://github.com/vercel-labs/skills) to install skills directly:

```bash
# Install all skills
npx skills add finnan444/skills

# Install specific skills
npx skills add finnan444/skills --skill skeleton-dev

# List available skills
npx skills add finnan444/skills --list
```

This automatically installs to your `.claude/skills/` directory.

## Contributing

Found a way to improve a skill? Have a new skill to suggest? PRs and issues welcome!

## License

[MIT](LICENSE) - Use these however you want.