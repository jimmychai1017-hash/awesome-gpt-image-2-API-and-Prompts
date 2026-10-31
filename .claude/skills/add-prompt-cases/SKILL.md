---
name: add-prompt-cases
description: Add a batch of new GPT Image 2 prompt cases to this repository — dedupe against the source registry, place and number them in README.md, update the matching cases/*.md pages, data/ingested_tweets.json, media, News and docs/update-log.md, run the verifier, then localize. Use when the user wants to add, ingest, or publish new prompt cases or a daily/weekly prompt batch.
---

# Add prompt cases

Follow `CLAUDE.md` (铁律) and `docs/maintenance.md`. This skill is the step order; those files are the rules.

## 0. Preflight

- `git status --short` and `git branch --show-current`. Unrelated changes present → stop and ask, or use an isolated worktree.
- `python3 scripts/verify_prompt_repo.py` must pass **before** you start, so any later failure is yours.
- The README files are ~1.1 MB each. Locate with `grep -n`, read slices by line number; never read a whole README.

## 1. Collect and review candidates

For each candidate, record: source URL, author handle + profile URL, verbatim prompt, category, title, media shape (output-only or input/output), media files.

Reject (and report the count and reason) anything that is:
- already in the registry: `grep -F "<status-id>" data/ingested_tweets.json`;
- missing a public prompt (showcase-only), an author, or verifiable media;
- deferred / unsure / duplicate / not a high-confidence selection.

Never fill a gap by inventing prompt text, authors, dates, or results. Freeze the batch and tell the user the selected / deferred / dropped counts before editing files.

Category → section → archive page:

| category | README anchor | archive |
|---|---|---|
| E-commerce Cases | `category-ecommerce` | `cases/ecommerce.md` |
| Ad Creative Cases | `category-ad-creative` | `cases/ad-creative.md` |
| Portrait & Photography Cases | `category-portrait` | `cases/portrait.md` |
| Poster & Illustration Cases | `category-poster` | `cases/poster.md` |
| Character Design Cases | `category-character` | `cases/character.md` |
| UI & Social Media Mockup Cases | `category-ui` | `cases/ui.md` |
| Comparison & Community Examples | `category-comparison` | `cases/comparison.md` |

## 2. Numbering — read before placing anything

Case numbers follow display order and must stay contiguous (`Case 1`…`Case N`). A new case appended to the end of its category section takes the number right after that section's last case, and **every later case in every later section shifts by +1**. Only cases added to the last section (Comparison) avoid a renumber.

If the batch causes a renumber:
- confirm with the user first;
- do it with a script, not by hand, across: all 11 README files (`### Case N:` headings and `<!-- Case N: ... -->` comments), matching `cases/*.md` and `cases/*_<locale>.md` entries whose source URL is in the authoritative set, and `case_anchor` values in `data/ingested_tweets.json` (anchor slug: `#case-<n>-<title-slug>-by-<handle-lowercase>`);
- leave prompt bodies and media untouched.

Bump `EXPECTED_CASE_COUNT` in `scripts/verify_prompt_repo.py` by the number of added cases.

## 3. Edit the English source

Copy the shape of the neighbouring cases exactly:

````markdown
<!-- Case N: <Title> (by @<handle>) -->
### Case N: [<Title>](<source-url>) (by [@<handle>](<profile-url>))

| Output |
| :----: |
| <a href="https://evolink.ai/gpt-image-2-prompts?utm_source=github&utm_medium=picture&utm_campaign=awesome-gpt-image-2-API-and-Prompts" target="_blank" rel="noopener noreferrer"><img src="images/<category>_case<k>/output.jpg" width="300" alt="GPT-Image-2 Prompt Example - <Title>"></a> |

**Prompt:**

```
<verbatim prompt>
```
````

Cases with several images use a `<table>` of `<td width="50%">` cells instead of the one-column table — copy an existing one (e.g. Case 6 in Ad Creative) rather than writing it from memory.

Then, in the same change:
1. Update the section's `> **K curated cases**` line, and the total in the `462_Curated_Cases` badge (line ~8) and the Introduction sentence (`library of 462 curated ...`).
2. Add the entry to the matching `cases/<category>.md` page, same shape and the same Case number.
3. Put media under a new `images/<category>_case<k>/` (next free `k` for that prefix — `ls images | grep '^<category>_case'`). No file over 25 MB; no raw video as visible media.
4. Append one record per case to `data/ingested_tweets.json` `records`, using the fields of the latest records: `tweet_url`, `author_handle`, `title`, `category`, `readme_file`, `case_anchor`, `image_dir`, `added_at` (ISO 8601, UTC).
5. Add a News line at the top of `## 📰 News` in the existing wording style.
6. Add a dated line to `docs/update-log.md` with the per-category counts.

## 4. English gate

```bash
python3 scripts/verify_prompt_repo.py
python3 -m json.tool data/ingested_tweets.json >/dev/null
git diff --check
```

All must pass before touching any localized file.

## 5. Localize

Run the `sync-localized-readmes` skill: insert the same cases at the same positions in all 10 `README_<locale>.md` and `cases/<category>_<locale>.md` files, update the same counters (localized section lines are `> **K curated cases**` without a link; the badge and Introduction total are translated text), translate the visible prose such as the News line, keep titles, prompt blocks, URLs and commands unchanged.

## 6. Finish

- Rerun the full validation block from `CLAUDE.md`, including the system-file scan.
- Review `git diff --stat` — only README*, cases/*, data/ingested_tweets.json, images/, docs/update-log.md and (if renumbered) scripts/verify_prompt_repo.py should change.
- Commit in the house style, e.g. `Add <Month> <day> GPT Image 2 prompt batch`.
- Tell the user what still needs a maintainer: R2 media migration, public link / UTM audit, rendered GitHub check.
