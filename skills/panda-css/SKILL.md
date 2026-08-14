---
name: panda-css
description: Build styles with Panda CSS. Use when creating, editing, or reviewing any code that uses Panda CSS — css(), cva(), sva(), recipes, patterns, tokens, semantic tokens, panda.config, theming, codegen, or JSX styled components. Also use when Panda emits class names but no CSS. Supports React, Vue, Svelte, Solid, and any framework with PostCSS.
---

# Panda CSS

## Process

1. **Package.** Confirm `@pandacss/dev` in the target package (monorepo: the app being edited). If it is missing, stop and tell the user. Done when you have the installed major and the package path.

2. **Config.** Read `panda.config.ts` (or `.js`/`.mjs`); if absent, ask whether to scaffold. Done when you have `outdir` (default `styled-system`), `include`, `jsxFramework`, and the import prefix that package already uses.

3. **Docs.** Fetch `https://panda-css.com/llms.txt`. Fetch only the section URLs that index lists for this task. Reuse the in-session copies unless the index changed. If the installed major does not match the docs' major, flag it before copying APIs. If the index is unreachable, fall back to `llms.txt/{overview,concepts,theming,utilities,customization,guides,references}` or `llms-full.txt`. Done when those pages are in context.

4. **Write or review.** Apply every rule below to the diff. Done when each rule holds.

## Rules

**Imports.** Runtime (`css`, `cva`, `sva`, recipes, patterns, `styled`) comes from `outdir`. Config authors (`defineConfig`, `defineRecipe`, `defineSlotRecipe`, `defineTokens`, …) come from `@pandacss/dev`. Copy the package's existing import prefix (alias vs relative). Treat `outdir` as a build artifact. Changing tokens, recipes, patterns, conditions, `jsxFramework`, or `outdir` requires codegen before the new types or runtime exist.

**Names.** Every token, recipe, and pattern name comes from this config (and its presets) or the generated types. Match the vocabulary already used in neighboring files.

**Extraction.** Panda emits CSS for style objects and recipe variants it can see at build time. Keep values statically analyzable. A runtime variable as a style value, or a config-recipe variant passed only as a prop, yields class names without CSS unless `staticCss` or a literal extracted call covers it. The file must sit inside `include`.

**Which API.** Use the primitive this package already uses for the same job. If none, pick from the Concepts docs after loading them. `styled` / the JSX factory only when `jsxFramework` is set.
