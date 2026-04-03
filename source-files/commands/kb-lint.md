---
name: kb-lint
description: Run health checks on a Knowledge Base wiki to find broken links, inconsistencies, and suggest improvements
args:
  - name: vault
    description: Vault name or path. Auto-detected from CWD if omitted.
    required: false
  - name: fix
    description: Auto-fix broken links and structural issues. Default false.
    required: false
    default: "false"
tags: [Knowledge Base, Lint, Quality]
---

# /kb-lint — Knowledge Base Health Check

Run structural and semantic health checks on the wiki.

## Workflow

1. **Detect the target vault**:
   - If `$vault` is provided, resolve it
   - Otherwise, run: `python "$HOME/.claude/scripts/kb_engine.py" detect --cwd "$PWD"`

2. **Run structural checks** (fast, deterministic):
   ```bash
   python "$HOME/.claude/scripts/kb_engine.py" validate-links --vault-path "<vault>"
   ```
   This finds broken `[[wikilinks]]` that don't resolve to any article.

3. **Delegate to kb-linter agent** for semantic checks:
   - Consistency between articles
   - Missing cross-references
   - Coverage gaps
   - New article candidates
   - Data integrity issues

4. **If `$fix` is "true"**: auto-fix what can be fixed:
   - Create stub articles for broken wikilinks
   - Add missing backlinks
   - Fix frontmatter issues

5. **Write lint report** to `_meta/lint-report.md`

6. **Present summary** to the user:
   - Critical issues count
   - Warnings count  
   - Suggestions count
   - Top 3 actionable items

## Notes

- Structural checks are instant; semantic checks take longer as the agent reads articles
- The lint report is viewable in Obsidian at `_meta/lint-report.md`
- Run `/kb-lint` periodically to keep the wiki healthy
- Use `/kb-lint --fix true` to auto-repair structural issues
