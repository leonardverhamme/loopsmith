---
name: gitignore-skill
description: Maintain `.gitignore` safely. Use when logs, test output, browser artifacts, local agent state, caches, build output, Graphify output, or temp files are cluttering `git status`, and the repo needs tighter ignore rules without hiding real source files.
---

# Gitignore Skill

## Stability

- Treat this skill as stable infrastructure.
- Do not edit this skill unless the user explicitly opens `$editskill` for it.

Use this skill to tighten `.gitignore` safely. The goal is to cut commit noise and token waste from junk files, not to hide source-of-truth files.

## Bare Invocation

If the user invokes `$gitignore-skill` with no meaningful extra instruction, inspect the repo and report:

1. the current ignore surface
2. the biggest junk classes still leaking into `git status`
3. the safest next `.gitignore` edits to make

## Required Workflow

1. Inspect the repo surface first:
   - root and nested `.gitignore`
   - `.git/info/exclude` when relevant
   - `git status --short`
   - `git status --short --ignored` when supported
   - `git ls-files` for suspicious tracked junk
   - the tool outputs creating noise: tests, Playwright, Graphify, coverage, build systems, temp folders, local caches
2. Load:
   - `references/patterns.md`
   - `references/tracked-junk.md`
3. Classify candidate paths:
   - local generated junk
   - generated output intentionally committed
   - source-of-truth files that must stay visible
4. Prefer narrow, path-specific ignore rules over broad globs.
5. Keep root `.gitignore` as the default home for repo-wide junk. Use nested `.gitignore` only when subtree ownership is real.
6. Validate with `git status --short` and `git check-ignore -v <path>` when needed.
7. If junk is already tracked, explain that `.gitignore` alone will not untrack it. Only propose or run `git rm --cached` when the user explicitly wants that cleanup or the repo contract is already obvious.
8. Report what was ignored, what remains tracked, and what was intentionally left visible.

## Default Posture

- Focus on local noise, not on hiding uncertainty.
- Treat local agent state, browser/test output, logs, caches, temp data, and Graphify output as likely ignore candidates unless the repo intentionally commits them.
- Prefer stable directories or exact paths over broad extension rules.
- Re-check whether a path is already covered before adding duplicate rules.

## Hard Rules

- Do not add blanket patterns like `*`, `*.json`, or `*.md` just to make status cleaner.
- Do not hide source code, migrations, fixtures, seeds, lockfiles, screenshots, docs, or snapshots by guesswork.
- Do not assume `dist/`, `build/`, `coverage/`, or `graphify-out/` are disposable; check repo intent first.
- Do not silently untrack committed files.
- Do not stop after editing `.gitignore`; verify that the rule matches the intended paths.

## References

- `references/patterns.md`
- `references/tracked-junk.md`
