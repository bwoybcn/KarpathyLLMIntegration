# Article Schema Reference

## Concept Article

```markdown
---
title: "Concept Name"
type: concept
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - "raw/web/source-file.md"
  - "raw/papers/paper-file.md"
tags:
  - primary-tag
  - secondary-tag
category: "[[Category Name]]"
aliases:
  - "Alternative Name"
  - "Abbreviation"
confidence: high | medium | low
---

# Concept Name

One-paragraph summary of this concept. Should be self-contained and understandable without reading the full article.

## Overview

Main explanation of the concept. Use [[wikilinks]] to related concepts. This section provides the core understanding.

## Key Points

- Important point with [[Related Concept]] links
- Another key insight from the sources
- Technical detail or specification

## Evidence and Sources

- From [[Source: Article Title]]: specific finding or claim
- From [[Source: Paper Title]]: supporting data or quote
- Conflicting view from [[Source: Other Article]]: alternative perspective

## Related Concepts

- [[Related Concept 1]] — how it relates (e.g., "prerequisite", "builds on", "contrasts with")
- [[Related Concept 2]] — relationship description

## Open Questions

- Unresolved question about this concept
- Area where sources disagree or data is insufficient
```

## Source Summary Article

```markdown
---
title: "Source: Original Article Title"
type: source-summary
created: YYYY-MM-DD
updated: YYYY-MM-DD
source_path: "raw/web/original-file.md"
source_url: "https://example.com/article"
source_type: web | paper | repo | note
author: "Author Name"
date_published: YYYY-MM-DD
date_ingested: YYYY-MM-DD
tags:
  - source
  - topic-tag
---

# Source: Original Article Title

## Summary

Two to three paragraph summary of the source's main content and contribution.

## Key Claims

- Claim 1 — links to [[Relevant Concept]]
- Claim 2 — links to [[Another Concept]]
- Claim 3 with supporting data

## Concepts Mentioned

- [[Concept A]] — how this source relates to it
- [[Concept B]] — what new information it provides

## Notable Quotes and Data

> Direct quote from the source if particularly important.

- Key statistic or data point
- Methodology detail worth preserving
```

## Category Article

```markdown
---
title: "Category Name"
type: category
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - category
parent_category: "[[Parent Category]]"
---

# Category Name

Brief description of what this category covers.

## Concepts

- [[Concept A]] — one-line description
- [[Concept B]] — one-line description
- [[Concept C]] — one-line description

## Subcategories

- [[Subcategory 1]]
- [[Subcategory 2]]
```

## Frontmatter Field Reference

| Field | Required | Types | Description |
|-------|----------|-------|-------------|
| `title` | Yes | all | Display name, matches `# H1` heading |
| `type` | Yes | all | `concept`, `source-summary`, or `category` |
| `created` | Yes | all | Date first created (YYYY-MM-DD) |
| `updated` | Yes | all | Date last modified (YYYY-MM-DD) |
| `sources` | Yes | concept | List of raw/ file paths that inform this article |
| `tags` | Yes | all | Topic tags for filtering and discovery |
| `category` | Yes | concept | Wikilink to the parent category |
| `aliases` | No | concept | Alternative names for wikilink resolution |
| `confidence` | No | concept | `high`, `medium`, or `low` |
| `source_path` | Yes | source-summary | Path to the raw source file |
| `source_url` | No | source-summary | Original URL if from web |
| `source_type` | Yes | source-summary | `web`, `paper`, `repo`, or `note` |
| `author` | No | source-summary | Source author |
| `date_published` | No | source-summary | When the source was published |
| `date_ingested` | Yes | source-summary | When it was added to raw/ |
| `parent_category` | No | category | Wikilink to parent category |
