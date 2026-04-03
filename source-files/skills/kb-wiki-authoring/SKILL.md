---
name: kb-wiki-authoring
description: Use when writing, editing, or merging wiki articles in an LLM Knowledge Base vault. Covers article schema, wikilink conventions, merge strategy, and index maintenance.
version: 1.0.0
tags: [Knowledge Base, Wiki, Obsidian, Writing]
---

# KB Wiki Authoring

Skill for writing and maintaining articles in a Karpathy-style LLM Knowledge Base.

## When to Activate

- Any time you create or edit a `.md` file inside `wiki/` of a KB vault
- During `/kb-compile` when processing raw sources into wiki articles
- During `/kb-lint` when fixing or improving articles
- When filing `/kb-query` output back into the wiki

## Vault Detection

A KB vault contains `_meta/compilation-state.json` and `raw/` at its root. The vault root also has `AGENTS.md` with KB-specific rules.

## Article Types

| Type | Location | Purpose |
|------|----------|---------|
| `concept` | `wiki/concepts/` | One article per concept/topic. The core of the wiki. |
| `source-summary` | `wiki/sources/` | One per raw source. Summarizes and links to concepts. |
| `category` | `wiki/categories/` | Groups related concepts. Links to all members. |
| `timeline` | `wiki/concepts/` | Chronological event sequence. Used for news/events research. |

## Article Schema

See `references/ARTICLE-SCHEMA.md` for full frontmatter and section templates.

**Key rules:**
1. Every article MUST have YAML frontmatter with `title`, `type`, `created`, `updated`, `sources`, `tags`, `category`
2. Use `[[wikilinks]]` for ALL cross-references between wiki articles
3. Wikilink targets must match an article's `title` frontmatter field exactly
4. Filename must be the kebab-case slug of the title: `attention-mechanism.md`
5. The `aliases` field lists alternative names that should also resolve to this article
6. The `confidence` field (high/medium/low) indicates how well-supported the article's claims are

## Wikilink Conventions

- Link format: `[[Article Title]]` or `[[Article Title|display text]]`
- Always link on first mention of a concept within each section
- Don't link the same concept multiple times in the same paragraph
- Category links use: `[[Category Name]]` in the `category` frontmatter field
- Source links use: `[[Source: Original Title]]`
- If a concept doesn't have an article yet, still link it — it becomes a candidate for future compilation

## Compilation Workflow

See `references/COMPILATION-PIPELINE.md` for the full pipeline.

**Per-source processing:**
1. Read the raw source document completely
2. Extract key concepts, claims, entities, relationships
3. Create `wiki/sources/{slugified-source-title}.md` with the source-summary schema
4. For each extracted concept:
   - Check if `wiki/concepts/{concept-slug}.md` exists
   - If YES → merge (see `references/MERGE-STRATEGY.md`)
   - If NO → create new concept article
5. Assign categories and update category pages

## Index Maintenance

See `references/INDEX-MAINTENANCE.md` for details.

After any article changes, these index files MUST be updated:
- `wiki/_index.md` — Master list of all articles with 1-line summaries
- `wiki/_categories.md` — Category tree with member links
- `wiki/_glossary.md` — Terms mapped to canonical article names
- `wiki/_backlinks.md` — Reverse link index (what links to each article)

The `kb_engine.py rebuild-index` script handles `_index.md` automatically. The LLM should update the others during compilation.

## Tag Taxonomy

Use hierarchical tags with `/` prefixes for structured filtering in Obsidian's tag pane:

| Prefix | Examples | Applied to |
|--------|----------|-----------|
| `#type/` | `#type/concept`, `#type/source`, `#type/timeline`, `#type/category` | All articles (auto) |
| `#confidence/` | `#confidence/high`, `#confidence/medium`, `#confidence/low` | Concept articles |
| `#source-type/` | `#source-type/paper`, `#source-type/web`, `#source-type/repo`, `#source-type/news` | Source summaries |
| `#topic/` | `#topic/machine-learning`, `#topic/attention` | All articles (domain-specific) |

Always include the `#type/` tag. Topic tags are in addition to the type tag.

## Obsidian Callouts

Use Obsidian callout syntax for visually distinct sections:

- `> [!abstract]` — Article summary paragraph (at the top)
- `> [!example]` — Key findings or notable data points
- `> [!question]` — Open questions and unresolved issues
- `> [!warning]` — Conflicting accounts or contradictions between sources
- `> [!tip]` — Key insights or important takeaways

## Embed Conventions

Use embeds to transclude related content inline:
- `![[Concept Name#Overview]]` — embed the Overview section of a related concept
- Only embed in the `## See Also` section at the end of articles
- Limit to 2-3 embeds per article to avoid clutter
- Embeds render inline in Obsidian — the reader sees the content without navigating away

## Quality Standards

- Every claim must be attributed to a source in the Evidence section
- Contradictory claims from different sources should BOTH be preserved with attribution
- Never delete information during a merge — only add, reorganize, or annotate
- Use `> [!question]` callouts for Open Questions rather than plain headings
- Summaries in `_index.md` must be under 150 characters
