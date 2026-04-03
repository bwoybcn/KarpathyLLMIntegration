# Getting Started

## Prerequisites

- **Claude Code** — installed and configured
- **Obsidian** — installed (for viewing the wiki)
- **Python 3** — for `kb_engine.py`
- **Defuddle CLI** — for web article ingestion
  ```bash
  npm install -g defuddle-cli
  ```

## Quick Start

### 1. Create your first knowledge base

```
/kb-new "Transformer Architecture"
```

This creates a vault at `D:\KnowledgeBases\transformer-architecture\` with the full directory structure and pre-configured Obsidian settings.

### 2. Open it in Obsidian

Open Obsidian → "Open folder as vault" → select `D:\KnowledgeBases\transformer-architecture\`.

On first open, Obsidian will ask you to trust community plugins (Dataview, Marp Slides). Click "Trust" to enable them.

### 3. Let the system find sources for you

```
/kb-research "transformer architecture and attention mechanisms"
```

This autonomously searches the web, evaluates candidate sources for quality and relevance, and ingests the best 3-8 into your vault's `raw/` directory. You can also target specific source types:

```
/kb-research "attention mechanisms" --type academic
```

For news topics, use `--type news` with a date range:

```
/kb-research "UK general election" --type news --date_range "2025-06-01 to 2025-07-31"
```

This uses news-specific search strategies (wire services, major outlets, analysis pieces), enforces multi-perspective sourcing (at least 2 outlets per event), and creates timeline articles for chronological event sequences.

### 3b. Or manually ingest specific sources

```
/kb-ingest https://jalammar.github.io/illustrated-transformer/
```

```
/kb-ingest https://arxiv.org/abs/1706.03762
```

This detects the arXiv URL and uses AlphaXiv to fetch a structured overview (falling back to PDF extraction if unavailable).

```
/kb-ingest D:\papers\attention-is-all-you-need.pdf
```

```
/kb-ingest https://github.com/huggingface/transformers
```

Each source is saved to `raw/` and you'll be nudged to compile.

### 4. Compile the wiki

```
/kb-compile
```

This reads all new sources, extracts concepts, creates wiki articles with `[[wikilinks]]`, and builds the index. It processes one source at a time for quality.

After compilation, check the wiki in Obsidian:
- Articles in `wiki/concepts/` and `wiki/sources/` with callout-formatted sections
- `wiki/_dashboards.md` — live Dataview dashboard showing article stats and gaps
- `wiki/_concept-map.canvas` — visual concept relationship map
- Graph view shows the full link structure, color-coded by folder
- Tag pane shows structured `type/`, `confidence/`, `topic/` hierarchy

### 5. Ask questions

```
/kb-query "How does multi-head attention differ from single-head attention?"
```

The agent reads the index, identifies relevant articles, and synthesizes an answer with `[[wikilink]]` citations.

### 6. Check health

```
/kb-lint
```

Finds broken links, missing cross-references, inconsistencies, and suggests new articles to write.

### 7. Generate outputs

```
/kb-output slides "Overview of Transformer Architecture"
```

```
/kb-output report "Comparison of attention mechanisms"
```

Outputs are saved to `outputs/` and viewable in Obsidian.

### 8. Auto-expand the wiki

```
/kb-expand
```

Reads the lint report's gaps, autonomously researches sources to fill them, and compiles the results. This is the "set it and forget it" command — run it periodically and the wiki grows itself.

For continuous expansion, combine with Claude Code's `/loop` command (if available):
```
/loop 30m /kb-expand --max_sources 3
```

### 9. Check status

```
/kb-status
```

Shows article count, word count, uncompiled sources, and health summary.

## Tips

### Working with multiple vaults

Each topic gets its own vault. You can `cd` into a vault directory and commands will auto-detect it, or specify the vault explicitly:

```
/kb-ingest https://example.com --vault transformer-architecture
```

List all vaults:
```bash
python ~/.claude/scripts/kb_engine.py list
```

### The compilation loop

The core workflow is a loop:
1. Ingest sources → 2. Compile → 3. Query → 4. File answers back → 5. Lint → repeat

Over time, the wiki grows richer and more interconnected.

### Filing outputs back

After a `/kb-query` or `/kb-output`, you can file the results back into the wiki as new articles. This is Karpathy's "explorations add up" principle — your questions and investigations enhance the knowledge base.

### Source priorities

When compiling multiple new sources, they're processed in this order:
1. Academic papers (most structured)
2. Web articles
3. Repo documentation
4. Personal notes

### Graph view

In Obsidian, open the Graph View to see the link structure. Colors are pre-configured:
- **Blue** — concept articles
- **Green** — source summaries
- **Orange** — categories
- **Gray** — raw sources
- **Purple** — outputs

### MarkItDown for PDFs

PDF ingestion uses the MarkItDown MCP server. If it's not working, verify it's in your `~/.claude/settings.json` under `mcpServers.markitdown`.

### Zotero integration

If you have Zotero configured, you can ingest papers by Zotero item key:
```
/kb-ingest ABCD1234
```

## Troubleshooting

**Dataview queries show as raw code** — Make sure Dataview is updated to the latest version. Go to Settings > Community plugins > Check for updates. Then switch to Reading view (Ctrl+E) to see rendered tables.

**"Not inside a KB vault"** — Either `cd` into a vault directory or use `--vault` to specify one.

**Compilation seems slow** — Sources are processed one at a time for merge quality. Large papers take longer.

**Broken wikilinks after compile** — Run `/kb-lint --fix true` to auto-create stub articles for missing links.

**Obsidian doesn't show plugins** — Make sure you clicked "Trust" when prompted about community plugins on first vault open.
