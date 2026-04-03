---
name: kb-new
description: Create a new Karpathy-style LLM Knowledge Base vault in D:\KnowledgeBases\
args:
  - name: topic
    description: Topic name for the knowledge base (e.g., "Transformer Architecture", "EEG Decoding")
    required: true
tags: [Knowledge Base, Obsidian, Setup]
---

# /kb-new — Create New Knowledge Base

Create a new knowledge base vault for a given topic.

## Workflow

1. Run the init script:
   ```bash
   python "$HOME/.claude/scripts/kb_engine.py" init --topic "$topic"
   ```

2. Verify the vault was created successfully by checking the JSON output for `"status": "created"`.

3. The vault is created at `D:\KnowledgeBases\{topic-slug}\` with:
   - Pre-configured `.obsidian/` (Dataview, Marp Slides, Graph View colors)
   - `AGENTS.md` with vault rules
   - `raw/` with subdirectories for web, papers, repos, notes
   - `wiki/` with concepts, sources, categories dirs and empty index files
   - `outputs/` for reports, slides, charts
   - `_meta/` with empty compilation state

4. Tell the user:
   - The vault path
   - How to open it in Obsidian: `obsidian://open?vault={topic-slug}` or open the folder manually
   - Suggest next steps: use `/kb-ingest` to add sources, then `/kb-compile` to build the wiki

## Notes

- Topic names are slugified for the filesystem (e.g., "Transformer Architecture" → "transformer-architecture")
- If the vault already exists, the script will error — inform the user
- The vault is a standalone Obsidian vault that can be opened independently
- Community plugins (Dataview, Marp) need to be trusted on first open in Obsidian
