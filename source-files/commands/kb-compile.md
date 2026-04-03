---
name: kb-compile
description: Compile new/modified raw sources into the wiki, creating and merging concept articles with wikilinks
args:
  - name: vault
    description: Vault name or path. Auto-detected from CWD if omitted.
    required: false
  - name: source
    description: Compile only this specific raw source file (path relative to vault). Compiles all new sources if omitted.
    required: false
tags: [Knowledge Base, Compile, Wiki]
---

# /kb-compile — Compile Raw Sources into Wiki

Incrementally compile new or modified raw sources into structured wiki articles.

## Workflow

1. **Detect the target vault**:
   - If `$vault` is provided, resolve it
   - Otherwise, run: `python "$HOME/.claude/scripts/kb_engine.py" detect --cwd "$PWD"`

2. **Find sources to compile**:
   - If `$source` is provided, compile only that file
   - Otherwise, run: `python "$HOME/.claude/scripts/kb_engine.py" diff --vault-path "<vault>"`
   - This returns JSON with `new`, `modified`, and `deleted` source lists
   - If nothing to compile, report "Wiki is up to date" and exit

3. **Compile each source** (one at a time, in order: papers → web → repos → notes):

   For each new/modified source, use the **kb-compiler agent**:

   a. Read the raw source file completely
   b. Extract key concepts, claims, entities, and relationships
   c. Create a source summary article at `wiki/sources/{slug}.md` following the source-summary schema
   d. For each concept extracted:
      - Check if `wiki/concepts/{concept-slug}.md` exists
      - If YES: read the existing article and MERGE new information (per MERGE-STRATEGY.md)
      - If NO: create a new concept article from the schema
   e. Assign concepts to categories, creating category pages as needed

   Use the `$kb-wiki-authoring` skill for all article writing.

4. **Rebuild indexes**:
   ```bash
   python "$HOME/.claude/scripts/kb_engine.py" rebuild-index --vault-path "<vault>"
   ```
   Then update `_categories.md`, `_glossary.md`, and `_backlinks.md` by reading all wiki articles.

5. **Validate links**:
   ```bash
   python "$HOME/.claude/scripts/kb_engine.py" validate-links --vault-path "<vault>"
   ```
   If broken links found, create stub articles or fix wikilink targets.

6. **Mark sources as compiled**:
   ```bash
   python "$HOME/.claude/scripts/kb_engine.py" hash-raw --vault-path "<vault>"
   ```

7. **Update stats**:
   ```bash
   python "$HOME/.claude/scripts/kb_engine.py" stats --vault-path "<vault>"
   ```

8. **Update concept map canvas**:
   Read all concept articles, extract their wikilinks to other concepts, and regenerate `wiki/_concept-map.canvas` as a JSON Canvas file where:
   - Each concept article is a `file` node pointing to `wiki/concepts/{slug}.md`
   - Each wikilink between concepts is an edge
   - Nodes are arranged in a grid layout (the user can rearrange in Obsidian)

9. **Report** to the user:
   - Number of sources processed
   - New articles created
   - Existing articles updated (merged)
   - Any broken links found and fixed
   - Current wiki stats (article count, word count)
   - Remind: open `_dashboards.md` in Obsidian for live Dataview views

## Important

- Process ONE source at a time for best merge quality
- Always preserve existing article content during merges — never delete
- Every claim must be attributed to its source
- Use `[[wikilinks]]` consistently throughout all articles
- Use Obsidian callouts (`> [!abstract]`, `> [!example]`, `> [!question]`, `> [!warning]`) for visual sections
- Use structured tags (`type/concept`, `confidence/high`, `topic/x`) for Dataview filtering
- Add `## See Also` with `![[Concept#Overview]]` embeds (2-3 max) for related concepts
- Follow the article schema strictly (see `$kb-wiki-authoring` skill)
