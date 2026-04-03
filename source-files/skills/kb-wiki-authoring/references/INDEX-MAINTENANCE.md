# Index Maintenance Reference

## Index Files

The wiki maintains four index files at `wiki/` root. These are critical for both Obsidian navigation and LLM context-loading.

### `_index.md` — Master Index

**Purpose**: Quick lookup of all articles with one-line summaries. The LLM reads this first when answering queries.

**Format**:
```markdown
---
title: Master Index
type: index
updated: YYYY-MM-DD
---

# Topic Name — Master Index

**N articles**

## Concepts

- [[Concept A]] — One-line summary under 150 chars
- [[Concept B]] — Another concise summary

## Source Summaries

- [[Source: Article Title]] — What this source covers
- [[Source: Paper Title]] — Key contribution

## Categories

- [[Category A]] — What this category groups
```

**Maintenance**: Run `kb_engine.py rebuild-index` after compilation. This reads all article frontmatter and regenerates the index automatically.

### `_categories.md` — Category Tree

**Purpose**: Hierarchical view of all categories and their member concepts.

**Format**:
```markdown
---
title: Categories
type: index
updated: YYYY-MM-DD
---

# Categories

## [[Top Category A]]
- [[Concept 1]]
- [[Concept 2]]

### [[Subcategory A1]]
- [[Concept 3]]

## [[Top Category B]]
- [[Concept 4]]
```

**Maintenance**: The LLM updates this during compilation when concepts are assigned to categories.

### `_glossary.md` — Term Dictionary

**Purpose**: Maps terms (including abbreviations, alternative names) to their canonical article names. Helps the LLM resolve ambiguous references.

**Format**:
```markdown
---
title: Glossary
type: index
updated: YYYY-MM-DD
---

# Glossary

| Term | Canonical Article |
|------|------------------|
| Attention | [[Attention Mechanism]] |
| Self-Attention | [[Attention Mechanism]] |
| MHA | [[Multi-Head Attention]] |
| BERT | [[BERT]] |
| Bidirectional Encoder | [[BERT]] |
```

**Maintenance**: The LLM adds entries during compilation whenever it encounters new terms or aliases.

### `_backlinks.md` — Reverse Link Index

**Purpose**: For each article, lists all articles that link TO it. Supplements Obsidian's built-in backlinks with an LLM-readable format.

**Format**:
```markdown
---
title: Backlinks
type: index
updated: YYYY-MM-DD
---

# Backlinks Index

## [[Attention Mechanism]]
Linked from: [[Transformer Architecture]], [[BERT]], [[Source: Attention Is All You Need]]

## [[BERT]]
Linked from: [[Transfer Learning]], [[Source: BERT Paper Summary]]
```

**Maintenance**: Rebuild by scanning all `[[wikilinks]]` across all wiki articles. Can be done by the LLM or by extending `kb_engine.py`.

## When to Update Indexes

- **After `/kb-compile`**: All four indexes should be refreshed
- **After `/kb-lint` fixes**: If articles were modified, rebuild `_index.md` and `_backlinks.md`
- **After filing `/kb-query` output**: If output was filed into wiki, update `_index.md`
- **Manual**: Run `kb_engine.py rebuild-index` any time for a fresh `_index.md`
