# Vendored third-party skills

These skills are copied in from their upstream repositories so every session of this repository gets them without a separate install. Upstream owns them; update by re-copying, not by editing in place.

| Path | Upstream | Commit | Version | License |
|---|---|---|---|---|
| `.claude/skills/impeccable/` | https://github.com/pbakaus/impeccable (`.claude/skills/impeccable`) | `d79ce9bd055737a5527ac0bef34b5d2655d54fd0` | 4.8.0 (engine launcher 0.1.18) | Apache-2.0 — `LICENSE`, `NOTICE.md` in the skill folder |
| `.claude/agents/impeccable-*.md` | same repository (`.claude/agents`) | same | — | Apache-2.0 |
| `.claude/skills/ui-ux-pro-max/` | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill (`.claude/skills/ui-ux-pro-max`) | `bf41cbc3ce63e30c922e58ef48741ba6133f9aa9` | — | MIT — `LICENSE` in the skill folder |

## Local changes

- **ui-ux-pro-max:** script paths in `SKILL.md` changed from the plugin-only `${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/…` to `.claude/skills/ui-ux-pro-max/…`, the form upstream's own `uipro init --ai claude` installer writes for a project install (commands run from the repository root). Upstream's `scripts/tests/` was dropped; it tests upstream's repository layout and does not run here.
- **Whitespace:** upstream files contain trailing whitespace. They are kept verbatim; the root `.gitattributes` marks these paths `-whitespace` so `git diff --check` skips them.
- **impeccable:** unchanged. Its design-detector hooks (`SessionStart`, `PostToolUse` on Edit/Write, `Stop`) were **not** installed. They would run on every edit in this Markdown repository and download the engine binary outside model approval. Run `npx impeccable install` yourself if you want them.

## Behaviour to know about

- **impeccable:** `scripts/impeccable` downloads a platform engine binary into `~/.impeccable/bin/` on first use, checked against `scripts/engine-checksums.txt`. When a new design starts it fetches visual directions from impeccable.style; anonymous telemetry about which direction was picked can be turned off with `DO_NOT_TRACK=1` or `npx impeccable telemetry off`.
- **ui-ux-pro-max:** `scripts/search.py` uses the Python 3 standard library only and makes no network calls.

## Updating

```bash
git clone --depth 1 https://github.com/pbakaus/impeccable.git /tmp/impeccable
git clone --depth 1 https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git /tmp/uiux
rm -rf .claude/skills/impeccable .claude/skills/ui-ux-pro-max .claude/agents/impeccable-*.md
cp -r /tmp/impeccable/.claude/skills/impeccable .claude/skills/
cp /tmp/impeccable/.claude/agents/impeccable-*.md .claude/agents/
cp /tmp/impeccable/LICENSE /tmp/impeccable/NOTICE.md .claude/skills/impeccable/
cp -r /tmp/uiux/.claude/skills/ui-ux-pro-max .claude/skills/
cp /tmp/uiux/LICENSE .claude/skills/ui-ux-pro-max/
rm -rf .claude/skills/ui-ux-pro-max/scripts/tests
sed -i 's#${CLAUDE_PLUGIN_ROOT}/\.claude/skills/ui-ux-pro-max/#.claude/skills/ui-ux-pro-max/#g' .claude/skills/ui-ux-pro-max/SKILL.md
```

Then update the commit hashes in the table above.
