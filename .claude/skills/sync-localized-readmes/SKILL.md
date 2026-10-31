---
name: sync-localized-readmes
description: Bring the 10 localized README_<locale>.md files and cases/*_<locale>.md pages in line with the English README.md after cases or public copy change, then prove parity (same case order and numbers, identical prompt blocks, no placeholder markers). Use after adding or renumbering cases, after editing visible README copy, or when asked to check or fix localization.
---

# Sync localized READMEs

Locales: `de es fr ja ko pt ru tr zh-CN zh-TW`. English `README.md` is the source; finish and verify it first.

## What stays identical in every locale

- Case order and numbers, `<!-- Case N: ... -->` comments, `### Case N: [Title](url) (by [@handle](url))` headings — titles stay in English.
- Everything inside code fences (prompt text), URLs, image paths, model IDs, commands, environment variables, `<a id="...">` anchors.

## What is translated

Visible prose only: Introduction, Quick Start, News lines, Menu labels, section intros, the prompt label (`**Prompt:**` is `**提示词:**`, `**プロンプト:**`, `**Промпт:**`, …), Contribute / Related / Acknowledge text. Copy the wording pattern from the locale's own existing lines — e.g. an existing News entry in that file — rather than translating from scratch, so tone and date formats stay consistent.

## Steps

1. Check the starting point: `python3 .claude/skills/sync-localized-readmes/check_locale_parity.py`. Note which locales already fail so you don't misattribute them.
2. For each changed case, find its position in English with `grep -n "^### Case <N>:" README.md` and insert the identical block at the same position in every `README_<locale>.md`, swapping in that locale's prompt label. Do the same in `cases/<category>_<locale>.md` when the English `cases/<category>.md` changed.
3. Update the locale's counters to match English: the section `> **K curated cases**` line, the total-cases badge, and the total in the Introduction sentence.
4. Translate any new visible prose (the News line for the batch, at the top of that locale's News section).
5. Re-run the checker until every locale prints `ok`, then the repository verifier:
   ```bash
   python3 .claude/skills/sync-localized-readmes/check_locale_parity.py
   python3 scripts/verify_prompt_repo.py
   git diff --check
   ```

## About `script/sync_multilingual_readmes.py`

It regenerates every localized README from the English file and keeps the human-maintained News/Menu sections by default. It writes all 10 files at once, so run it only when the user explicitly asks, review `git diff --stat` and spot-check each locale afterwards, and never pass `--rewrite-protected-sections` unless the user names that flag.

## Done means

- Parity checker exits 0 and the verifier prints `ok: True`.
- No TODO, translation-pending marker, or untranslated scaffolding was added.
- The final report names any locale text you could not translate confidently, so a maintainer can review it.
