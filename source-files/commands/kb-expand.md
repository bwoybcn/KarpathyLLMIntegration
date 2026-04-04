---
name: kb-expand
description: Automatically identify knowledge gaps in the wiki and research sources to fill them
args:
  - name: vault
    description: Vault name or path. Auto-detected from CWD if omitted.
    required: false
  - name: max_sources
    description: Maximum total sources to ingest across all gaps. Default 10.
    required: false
    default: "10"
tags: [Knowledge Base, Research, Autonomous, Expand]
---

# /kb-expand — Auto-Expand the Knowledge Base

Identify gaps in the wiki and autonomously research sources to fill them.

## Workflow

1. **Detect the target vault**:
   - If `$vault` is provided, resolve it
   - Otherwise, run: `python "$HOME/.claude/scripts/kb_engine.py" detect --cwd "$PWD"`

2. **Run a lint to find gaps**:
   - If `_meta/lint-report.md` doesn't exist or is stale, run `/kb-lint` first
   - Read the lint report's "Data Gaps" and "Suggestions" sections
   - Also check for broken wikilinks (concepts referenced but not yet written about)

3. **Prioritize gaps**:
   - Broken wikilinks (concepts mentioned but no article exists) — highest priority
   - Explicit data gap suggestions from the linter
   - Low-confidence articles that need more sources
   - Categories with very few members

4. **For each gap** (up to 3-4 gaps, budget `$max_sources` across them):
   - Run `/kb-research` with the gap topic
   - Compile the new sources into the wiki
   - The wiki grows and the gap shrinks

5. **Final lint** to verify improvements:
   ```bash
   python "$HOME/.claude/scripts/kb_engine.py" stats --vault-path "<vault>"
   ```

6. **Log the expansion** — append a dated entry to `_meta/expansion-log.md`:
   ```markdown
   ## {date} — Expansion
   - Gaps targeted: {list}
   - Sources ingested: {count}
   - Articles created: {count}
   - Articles merged: {count}
   - Before: {article count} articles, {word count} words
   - After: {article count} articles, {word count} words
   ```
   Create the file if it doesn't exist. Always append, never overwrite.

7. **Report** what was expanded:
   ```
   Wiki expanded:
   - Researched 3 gap topics
   - Ingested 8 new sources
   - Created 12 new concept articles
   - Wiki now: X articles, Y words (was: A articles, B words)
   
   Remaining gaps: [list if any]
   ```

## Notes

- This is the "set it and forget it" command — it autonomously grows the wiki
- Combines /kb-lint → /kb-research → /kb-compile in a loop
- Budget-aware: respects `$max_sources` to control cost
- Can be used with `/loop` for periodic expansion: `/loop 30m /kb-expand --max_sources 3`
- Each expansion cycle makes the wiki richer and the next lint more useful
