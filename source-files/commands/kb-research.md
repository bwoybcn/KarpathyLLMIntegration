---
name: kb-research
description: Autonomously search the web for sources on a topic, evaluate quality, and ingest the best ones into the Knowledge Base vault
args:
  - name: topic
    description: Research topic or question to find sources for
    required: true
  - name: vault
    description: Vault name or path. Auto-detected from CWD if omitted.
    required: false
  - name: max_sources
    description: Maximum number of sources to ingest. Default 5.
    required: false
    default: "5"
  - name: type
    description: "Preferred source type: any, academic, web, repos, news. Default any."
    required: false
    default: "any"
  - name: date_range
    description: "Date range filter, e.g. '2026-03-01 to 2026-03-31' or 'last 7 days' or '2025'. Useful for news research."
    required: false
tags: [Knowledge Base, Research, Autonomous, Web Search]
---

# /kb-research — Autonomous Source Discovery and Ingestion

Search the web for high-quality sources on a topic and ingest them into the vault.

## Workflow

1. **Detect the target vault**:
   - If `$vault` is provided, resolve it
   - Otherwise, run: `python "$HOME/.claude/scripts/kb_engine.py" detect --cwd "$PWD"`
   - If no vault found, ask which vault to use or suggest `/kb-new`

2. **Check current wiki coverage**:
   - Read `wiki/_index.md` to understand existing coverage
   - Read `_meta/lint-report.md` if it exists for known data gaps
   - This prevents wasting searches on topics already well-covered

3. **Delegate to kb-researcher agent** with:
   - The research topic (`$topic`)
   - The vault path
   - Max sources to ingest (`$max_sources`)
   - Preferred source type (`$type`):
     - `any` — all source types
     - `academic` — prefer arXiv papers, surveys, peer-reviewed work
     - `web` — prefer blog posts, tutorials, documentation
     - `repos` — prefer GitHub repos, code documentation
     - `news` — prefer news outlets, use date-restricted searches, seek multiple perspectives
   - Date range (`$date_range`): if provided, restrict searches to this period

4. **The agent will**:
   a. Run multiple web searches with varied queries
   b. Evaluate 10-20 candidate sources for quality/relevance/novelty
   c. Ingest the top 3-8 sources into `raw/` with proper frontmatter
   d. Verify each ingested file has real content

5. **After research completes**, report to the user:
   - How many sources were found and ingested
   - List of ingested sources with quality ratings
   - List of skipped sources with reasons
   - Suggest running `/kb-compile` to process them

6. **Optionally auto-compile**: If the user wants, immediately run `/kb-compile` to process the new sources into wiki articles.

## Examples

```
/kb-research "transformer architecture and attention mechanisms"
```

```
/kb-research "EEG signal processing for brain-computer interfaces" --type academic
```

```
/kb-research "Rust async runtime internals" --type repos --max_sources 3
```

```
/kb-research "UK general election" --type news --date_range "2025-06-01 to 2025-07-31"
```

```
/kb-research "OpenAI leadership changes" --type news --date_range "last 30 days"
```

## Notes

- Uses WebSearch to find candidates, then defuddle/AlphaXiv/WebFetch to extract content
- Quality-first: skips paywalled, shallow, or duplicate content
- Checks existing wiki to avoid redundant ingestion
- For academic topics, prefers arXiv papers via AlphaXiv over blog summaries
- For news topics, seeks multiple perspectives and creates timeline articles
- Date ranges are passed to search queries (e.g. `after:2026-03-01 before:2026-03-31`)
- Each research run typically takes 1-3 minutes depending on topic breadth
- Use `$kb-source-ingestion` and `$alphaxiv-paper-lookup` skills for ingestion patterns
