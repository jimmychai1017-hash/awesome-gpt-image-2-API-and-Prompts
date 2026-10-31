#!/usr/bin/env python3
"""Compare every localized README with README.md, case by case.

Checks, per locale: same ordered list of (case number, source URL), identical
prompt code blocks, and no leftover TODO / translation-pending markers.
Read-only. Exit code 1 when any locale differs.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOCALES = ["de", "es", "fr", "ja", "ko", "pt", "ru", "tr", "zh-CN", "zh-TW"]
HEADING_RE = re.compile(r"^### Case (\d+): \[.+?\]\((https?://[^)]+)\)", re.MULTILINE)
# Scaffolding markers only; plain words like "translated" inside prompts are fine.
PLACEHOLDER_RE = re.compile(r"\bTODO\b|\bTBD\b|\[TRANSLATE|(?i:translation[- ]pending)|待翻译|待翻譯|未翻訳")


def cases(text: str) -> list[tuple[int, str]]:
    return [(int(n), url) for n, url in HEADING_RE.findall(text)]


def prompt_blocks(text: str) -> dict[int, list[str]]:
    """Map each case number to the fenced code blocks in its section.

    Labels such as **Prompt:** are translated per locale, so blocks are
    collected by position under each '### Case N:' heading instead.
    """
    blocks: dict[int, list[str]] = {}
    current = None
    fence = ""
    body: list[str] = []
    for line in text.splitlines():
        if fence:
            if re.match(r"^ {0,3}" + re.escape(fence) + r"\s*$", line):
                if current is not None:
                    blocks.setdefault(current, []).append("\n".join(body))
                fence = ""
            else:
                body.append(line)
            continue
        opening = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if opening:
            fence = opening.group(1)
            body = []
            continue
        heading = re.match(r"^### Case (\d+):", line)
        if heading:
            current = int(heading.group(1))
        elif line.startswith("## "):
            current = None
    return blocks


def main() -> int:
    base = (ROOT / "README.md").read_text(encoding="utf-8")
    base_cases = cases(base)
    base_prompts = prompt_blocks(base)
    print(f"README.md: {len(base_cases)} cases, {sum(map(len, base_prompts.values()))} code blocks")
    failed = False

    for locale in LOCALES:
        path = ROOT / f"README_{locale}.md"
        text = path.read_text(encoding="utf-8")
        problems = []

        loc_cases = cases(text)
        if loc_cases != base_cases:
            problems.append(f"case list differs ({len(loc_cases)} vs {len(base_cases)})")
            for i, (a, b) in enumerate(zip(base_cases, loc_cases)):
                if a != b:
                    problems.append(f"  first difference at position {i + 1}: expected {a}, found {b}")
                    break

        loc_prompts = prompt_blocks(text)
        changed = sorted(n for n in set(base_prompts) | set(loc_prompts) if base_prompts.get(n) != loc_prompts.get(n))
        if changed:
            shown = ", ".join(f"Case {n}" for n in changed[:10])
            more = f" (+{len(changed) - 10} more)" if len(changed) > 10 else ""
            problems.append(f"code blocks differ from README.md in {len(changed)} cases: {shown}{more}")

        hits = [m.group(0) for m in PLACEHOLDER_RE.finditer(text)]
        base_hits = [m.group(0) for m in PLACEHOLDER_RE.finditer(base)]
        if len(hits) > len(base_hits):
            problems.append(f"{len(hits) - len(base_hits)} more TODO/placeholder markers than README.md")

        status = "ok" if not problems else "FAIL"
        print(f"{path.name}: {status}")
        for line in problems:
            print(f"  {line}")
        failed = failed or bool(problems)

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
