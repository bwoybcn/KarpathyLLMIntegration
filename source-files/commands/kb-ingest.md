---
name: kb-ingest
description: Ingest a source (URL, file path, or Zotero reference) into a Knowledge Base vault's raw/ directory
args:
  - name: source
    description: URL, file path, or Zotero item key to ingest
    required: true
  - name: vault
    description: Vault name or path. Auto-detected from CWD if omitted.
    required: false
tags: [Knowledge Base, Ingest, Data Pipeline]
---

# /kb-ingest — Ingest Source into Knowledge Base

Ingest an external source into the raw/ directory of a KB vault.

## Workflow

1. **Detect the target vault**:
   - If `$vault` is provided, resolve it (check `D:\KnowledgeBases\{vault}\` or use as path)
   - Otherwise, run: `python "$HOME/.claude/scripts/kb_engine.py" detect --cwd "$PWD"`
   - If no vault found, ask the user which vault to use (list with `kb_engine.py list`)

2. **Classify the source** (`$source`):
   - If it starts with `http://` or `https://` → **web article**
   - If it ends with `.pdf`, `.docx`, `.pptx` → **document** (use MarkItDown MCP)
   - If it contains `github.com` → **repo**
   - If it ends with `.md` → **markdown note**
   - If it looks like a Zotero key (alphanumeric, 8 chars) → **Zotero item**
   - Otherwise → ask the user to clarify

3. **Process by type**:

   **Web article**:
   ```bash
   defuddle parse "$source" --md -o "<vault>/raw/web/<slug>.md"
   ```
   Then read the output file, add YAML frontmatter with source_url, date_ingested, title.

   **PDF/Office document**:
   Use MarkItDown MCP: `mcp__markitdown__convert_to_markdown` with the file path.
   Save output to `<vault>/raw/papers/<slug>.md` with frontmatter.

   **GitHub repo**:
   Fetch README and key docs using `defuddle parse` on the repo URL, or clone and extract.
   Save to `<vault>/raw/repos/<repo-slug>.md`.

   **Markdown note**:
   Copy the file to `<vault>/raw/notes/<filename>.md`.
   Add frontmatter if missing.

   **Zotero item**:
   Use Zotero MCP tools to fetch metadata and full text.
   Save to `<vault>/raw/papers/<slug>.md` with full bibliographic frontmatter.

4. **Verify** the file was saved correctly by reading it.

5. **Report** to the user:
   - What was ingested and where it was saved
   - File size / word count
   - Suggest running `/kb-compile` to process it into the wiki

## Important

- Use the `$kb-source-ingestion` skill for source type handling patterns
- Always add YAML frontmatter with at minimum: `source_url` (if applicable), `source_type`, `date_ingested`, `title`
- Slugify filenames: lowercase, hyphens, no special chars
- If defuddle is not installed, install it: `npm install -g defuddle-cli`
- For MarkItDown, check the MCP server is available before attempting conversion
