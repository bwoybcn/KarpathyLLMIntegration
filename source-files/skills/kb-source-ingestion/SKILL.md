---
name: kb-source-ingestion
description: Use when ingesting external content into a Knowledge Base vault's raw/ directory. Covers web articles (defuddle), PDFs (MarkItDown MCP), academic papers (Zotero), and repo documentation.
version: 1.0.0
tags: [Knowledge Base, Ingest, Data Pipeline]
---

# KB Source Ingestion

Skill for converting external sources into clean markdown files in a KB vault's `raw/` directory.

## When to Activate

- During `/kb-ingest` when processing a URL, file path, or Zotero reference
- When manually adding sources to a KB vault

## Source Type Detection

| Input | Type | Tool | Destination |
|-------|------|------|-------------|
| `https://...` (web URL) | Web article | Defuddle CLI | `raw/web/` |
| `arxiv.org/abs/...` URL | arXiv paper | AlphaXiv skill | `raw/papers/` |
| `*.pdf` path | PDF document | MarkItDown MCP | `raw/papers/` |
| `*.docx`, `*.pptx` path | Office doc | MarkItDown MCP | `raw/papers/` |
| Zotero key/collection | Paper | Zotero MCP | `raw/papers/` |
| `*.md` path | Markdown note | File copy | `raw/notes/` |
| GitHub repo URL | Repository | Clone + extract | `raw/repos/` |

## Web Articles (Defuddle)

```bash
defuddle parse "<url>" --md -o "raw/web/<slug>.md"
```

After extraction:
1. Add YAML frontmatter with source metadata:
   ```yaml
   ---
   source_url: "https://example.com/article"
   source_type: web
   author: "Author if available"
   date_published: "YYYY-MM-DD if available"
   date_ingested: "YYYY-MM-DD"
   title: "Article Title"
   ---
   ```
2. Download referenced images to `raw/web/images/` and update image paths
3. Ensure all content is preserved — defuddle removes navigation/ads but keeps article body

## PDF/Office Documents (MarkItDown MCP)

Use the MarkItDown MCP server to convert:
```
mcp__markitdown__convert_to_markdown(path="<file_path>")
```

After conversion:
1. Save the markdown output to `raw/papers/<slug>.md`
2. Add frontmatter with source metadata
3. For academic papers, extract: title, authors, abstract, date if possible

## arXiv Papers (AlphaXiv)

For arXiv URLs or paper IDs, use the `alphaxiv-paper-lookup` skill as the preferred ingestion path — it returns a structured markdown overview that's richer than raw PDF extraction:

```bash
curl -s "https://alphaxiv.org/overview/{PAPER_ID}.md"
```

If the overview isn't available (404), fall back to the full text:
```bash
curl -s "https://alphaxiv.org/abs/{PAPER_ID}.md"
```

Save to `raw/papers/{paper-id}.md` with frontmatter including the arXiv ID and URL.

If both AlphaXiv endpoints 404, fall back to MarkItDown MCP on the PDF at `https://arxiv.org/pdf/{PAPER_ID}`.

## Academic Papers (Zotero)

Use the Zotero MCP server:
1. `mcp__zotero__get_item` or `mcp__zotero__search_items` to find the paper
2. `mcp__zotero__get_fulltext` to get full text if available
3. Save to `raw/papers/<slug>.md` with frontmatter including DOI, authors, venue

## Repo Documentation

For GitHub repo URLs:
1. Clone or fetch the repo's README and key docs
2. Extract README.md, relevant documentation files
3. Save to `raw/repos/<repo-name>.md` with combined content
4. Include repo URL, description, and key file paths in frontmatter

## Filename Convention

All raw files use kebab-case slugs:
- Web: `raw/web/attention-is-all-you-need-blog.md`
- Papers: `raw/papers/vaswani-2017-attention.md`
- Repos: `raw/repos/huggingface-transformers.md`
- Notes: `raw/notes/my-thoughts-on-attention.md`

## Post-Ingestion

After saving any raw file:
1. The file is ready for compilation via `/kb-compile`
2. The `kb_engine.py diff` command will detect it as a NEW source
3. No manual registration is needed — the diff system uses file hashing
