---
name: skeleton-dev
description: Build UI with Skeleton UI v4 (any framework). Use when creating, editing, or reviewing any component that uses Skeleton UI — buttons, modals, tabs, navigation, forms, cards, avatars, etc. Also use when questions involve Skeleton presets, color pairings, composed component patterns, or theming. Supports Svelte, React, and framework-agnostic usage.
---

# Skeleton Dev

Reference Skeleton UI v4 LLM-optimized docs before writing or reviewing Skeleton components.

## Docs Sources

First fetch `https://www.skeleton.dev/llms.txt` — this is the comprehensive index of all available LLM docs.

Then detect the framework from the project (package.json, file extensions, imports) and fetch the matching full docs:

| Framework | URL |
|-----------|-----|
| Svelte | `https://www.skeleton.dev/llms-svelte.txt` |
| React | `https://www.skeleton.dev/llms-react.txt` |

Use WebFetch to retrieve the correct reference **before starting any task**.

## Usage

1. Fetch `llms.txt` index to check for any new/updated doc URLs
2. Detect framework from the project context
3. Fetch the matching framework-specific docs
4. Read the relevant sections for the components needed
5. Write or review code following the documented patterns
