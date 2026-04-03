# Compilation Pipeline Reference

## Overview

Compilation transforms raw source documents into structured wiki articles. It is incremental — only new or modified sources are processed.

## Pipeline Stages

### Stage 1: Diff Detection

Run `kb_engine.py diff --vault-path <path>` to identify:
- **NEW**: Files in `raw/` not yet in `compilation-state.json`
- **MODIFIED**: Files whose hash differs from the stored hash
- **DELETED**: Files in state but missing from disk

### Stage 2: Per-Source Processing

For each new or modified source, the kb-compiler agent:

1. **Read** the full raw source document
2. **Extract** key information:
   - Main concepts discussed (nouns, technical terms, named entities)
   - Claims and findings (assertions, data points, conclusions)
   - Relationships between concepts (X depends on Y, X is a type of Y)
   - Categories the content falls under
3. **Create source summary** at `wiki/sources/{slug}.md`:
   - Follows the source-summary schema
   - Links to all concepts mentioned
   - Preserves key quotes and data points
4. **For each concept extracted**:
   - Slugify the concept name to get the filename
   - Check if `wiki/concepts/{slug}.md` exists
   - If it exists → perform a MERGE (see MERGE-STRATEGY.md)
   - If it doesn't exist → create a new concept article from the schema
5. **Assign categories**:
   - Determine which category(ies) each concept belongs to
   - Create `wiki/categories/{category-slug}.md` if it doesn't exist
   - Add the concept to the category's member list

### Stage 3: Index Rebuild

After all sources are processed:

1. Run `kb_engine.py rebuild-index --vault-path <path>` to regenerate `_index.md`
2. Update `_categories.md` with the full category tree
3. Update `_glossary.md` with any new terms → canonical article mappings
4. Update `_backlinks.md` by scanning all `[[wikilinks]]` in all articles

### Stage 4: Validation

Run `kb_engine.py validate-links --vault-path <path>` to catch:
- Broken wikilinks (target article doesn't exist)
- Orphan articles (no incoming links from any other article)

Fix broken links by:
- Creating stub articles for missing concepts
- Correcting typos in wikilink targets
- Adding aliases to handle variant names

### Stage 5: State Update

Run `kb_engine.py hash-raw --vault-path <path>` to mark all processed sources as compiled.

## Processing Order

When multiple new sources exist, process them in this order:
1. Papers and academic sources first (most structured, best concept extraction)
2. Web articles second
3. Repo documentation third
4. Personal notes last (may reference concepts from other sources)

This order ensures concepts are well-defined before less-structured sources reference them.

## Batch Size

Process one source at a time to keep context focused. After each source:
- Write the source summary
- Create/merge all concept articles
- Move to the next source

Do NOT try to process all sources in one pass — the merge quality degrades with too many simultaneous changes.
