# LLM Knowledge Base System

A Karpathy-style LLM knowledge base system built on Claude Code and Obsidian. Raw sources (articles, papers, repos, notes) are ingested, compiled by an LLM into a structured markdown wiki with `[[wikilinks]]`, then queried, linted, and enhanced over time — all viewable in Obsidian.

Inspired by [Andrej Karpathy's approach](https://x.com/karpathy/status/2039805659525644595) to using LLMs for personal knowledge bases.

## Architecture

```
/kb-research → Sources → /kb-ingest → raw/ → /kb-compile → wiki/ → /kb-query, /kb-lint → outputs/
    ↑                                                             ↑_____ filed back _____↓
    └──────────────────── /kb-expand (auto-fill gaps) ────────────┘
```

Each knowledge base is a standalone Obsidian vault at `D:\KnowledgeBases\{topic}\`.

## Commands

| Command | Description |
|---------|-------------|
| `/kb-new {topic}` | Create a new knowledge base vault |
| `/kb-research {topic}` | Autonomously search the web, evaluate, and ingest sources. Supports `--type news` and `--date_range` |
| `/kb-ingest {url\|path}` | Manually ingest a specific source |
| `/kb-compile` | Compile raw sources into wiki articles with wikilinks |
| `/kb-query {question}` | Ask a question against the wiki (answer auto-saved to vault) |
| `/kb-lint` | Run health checks on the wiki |
| `/kb-expand` | Auto-identify gaps and research sources to fill them |
| `/kb-status` | Show vault statistics and health |
| `/kb-output {format}` | Generate slides, reports, or charts from wiki content |

## Vault Structure

```
D:\KnowledgeBases\{topic}\
├── .obsidian/          # Pre-configured (Dataview, Marp, Graph View)
├── AGENTS.md           # Claude Code rules for this vault
├── raw/                # Source documents
│   ├── web/            # Web articles (via defuddle)
│   ├── papers/         # PDFs/papers (via MarkItDown, Zotero)
│   ├── repos/          # Repo documentation
│   └── notes/          # Personal notes
├── wiki/               # LLM-compiled knowledge articles
│   ├── concepts/       # One article per concept
│   ├── sources/        # Per-source summaries
│   ├── categories/     # Category index pages
│   ├── _index.md       # Master index
│   ├── _categories.md  # Category tree
│   ├── _glossary.md    # Term → article mappings
│   ├── _backlinks.md   # Reverse link index
│   ├── _dashboards.md  # Live Dataview queries (control panel)
│   └── _concept-map.canvas  # Visual concept map
├── outputs/            # Generated deliverables
│   ├── reports/        # Markdown reports
│   ├── slides/         # Marp slide decks
│   └── charts/         # Matplotlib visualizations
└── _meta/              # Compilation state & metadata
    ├── compilation-state.json
    ├── stats.md
    ├── lint-report.md
    ├── research-log.md     # Append-only research history
    ├── compilation-log.md  # Append-only compile history
    ├── lint-history.md     # Lint trends over time
    ├── expansion-log.md    # Expansion history
    └── stats-history.md    # Timestamped growth table
```

## Components

| Type | Name | Purpose |
|------|------|---------|
| Script | `kb_engine.py` | Deterministic operations (init, diff, validate, stats) |
| Skill | `kb-wiki-authoring` | Article schema, merge strategy, index maintenance |
| Skill | `kb-source-ingestion` | Source type detection and conversion patterns |
| Agent | `kb-compiler` | Compiles raw sources into wiki articles |
| Agent | `kb-query-agent` | Researches answers against the wiki |
| Agent | `kb-linter` | Semantic health checks and improvement suggestions |
| Agent | `kb-researcher` | Autonomously finds and ingests quality sources |
| Hook | `kb-auto-compile-check.js` | Nudges to compile when files added to raw/ |

## Ingestion Tools

| Source Type | Tool | Destination |
|-------------|------|-------------|
| Web articles | Defuddle CLI | `raw/web/` |
| arXiv papers | AlphaXiv (structured overview) | `raw/papers/` |
| PDFs, DOCX, PPTX | MarkItDown MCP | `raw/papers/` |
| Academic papers | Zotero MCP | `raw/papers/` |
| GitHub repos | Defuddle / clone | `raw/repos/` |
| Markdown notes | File copy | `raw/notes/` |

## Key Principles

- **LLM writes the wiki** — you rarely edit articles manually
- **Incremental compilation** — only new/modified sources are processed
- **Never delete** — merges add information, contradictions are preserved with attribution
- **Everything linked** — `[[wikilinks]]` throughout, viewable in Obsidian's graph view
- **Explorations add up** — query answers auto-saved, all operations logged to `_meta/`
- **Works for any topic** — academic research, news stories, technical docs, general knowledge
- **News-aware** — date range filtering, timeline articles, multi-perspective sourcing, event deduplication
- **Obsidian-native** — callouts, Dataview dashboards, structured tags, Canvas concept maps, embeds

## File Locations

```
~/.claude/
├── scripts/kb_engine.py
├── skills/kb-wiki-authoring/
├── skills/kb-source-ingestion/
├── skills/alphaxiv-paper-lookup/
├── commands/kb-{new,research,ingest,compile,query,lint,expand,status,output}.md
├── agents/kb-{compiler,query-agent,linter,researcher}.md
├── hooks/kb-auto-compile-check.js
└── templates/kb-vault-template/
```
