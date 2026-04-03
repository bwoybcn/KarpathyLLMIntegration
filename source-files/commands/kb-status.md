---
name: kb-status
description: Show the current status and statistics of a Knowledge Base vault
args:
  - name: vault
    description: Vault name or path. Auto-detected from CWD if omitted.
    required: false
tags: [Knowledge Base, Status, Dashboard]
---

# /kb-status — Knowledge Base Status Dashboard

Show a summary of the knowledge base's current state.

## Workflow

1. **Detect the target vault**:
   - If `$vault` is provided, resolve it
   - Otherwise, run: `python "$HOME/.claude/scripts/kb_engine.py" detect --cwd "$PWD"`
   - If no vault specified or detected, list all vaults: `python "$HOME/.claude/scripts/kb_engine.py" list`

2. **Gather statistics** (includes uncompiled count and broken link count):
   ```bash
   python "$HOME/.claude/scripts/kb_engine.py" stats --vault-path "<vault>"
   ```
   This single command returns all metrics including uncompiled sources and broken links.

3. **Present a dashboard** to the user:

   ```
   Knowledge Base: {topic}
   Path: {vault_path}

   Stats:
   - Raw sources: X
   - Wiki articles: Y (Z concepts, W source summaries)
   - Total words: N
   - Categories: M

   Health:
   - Uncompiled sources: X
   - Broken wikilinks: Y

   Suggestions:
   - [if uncompiled > 0] Run /kb-compile to process new sources
   - [if broken > 0] Run /kb-lint to fix broken links
   ```
