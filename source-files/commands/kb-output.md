---
name: kb-output
description: Generate outputs (slides, reports, charts) from Knowledge Base wiki content
args:
  - name: format
    description: "Output format: slides, report, chart, or summary"
    required: true
  - name: topic
    description: Topic or question to generate output for. Uses recent query context if omitted.
    required: false
  - name: vault
    description: Vault name or path. Auto-detected from CWD if omitted.
    required: false
tags: [Knowledge Base, Output, Slides, Report]
---

# /kb-output — Generate Knowledge Base Outputs

Generate deliverables from the wiki in various formats.

## Workflow

1. **Detect the target vault**:
   - If `$vault` is provided, resolve it
   - Otherwise, run: `python "$HOME/.claude/scripts/kb_engine.py" detect --cwd "$PWD"`

2. **Determine the topic**:
   - If `$topic` is provided, use it
   - Otherwise, ask the user what they want to generate output for

3. **Read relevant wiki articles** (same process as `/kb-query` — consult the index, read relevant articles)

4. **Generate output by format**:

   ### `slides` — Marp slide deck
   Create a Marp-format markdown file at `outputs/slides/{slug}.md`:
   ```markdown
   ---
   marp: true
   theme: default
   paginate: true
   ---

   # {Title}

   ---

   ## Key Concept 1

   - Point with context
   - Another point

   ---

   ## Key Concept 2
   ...
   ```

   ### `report` — Long-form markdown report
   Create `outputs/reports/{slug}.md` with:
   - Executive summary
   - Detailed sections for each relevant concept
   - Evidence and citations via [[wikilinks]]
   - Conclusions and open questions

   ### `chart` — Data visualization
   Generate a Python matplotlib script and run it to create a PNG:
   - Save script to `outputs/charts/{slug}.py`
   - Run: `python outputs/charts/{slug}.py`
   - Save PNG to `outputs/charts/{slug}.png`
   - The chart should be viewable in Obsidian

   ### `summary` — Executive summary
   Create a concise 1-page summary at `outputs/reports/{slug}-summary.md`

5. **Report** to the user:
   - Output file path
   - Suggest opening in Obsidian
   - Ask if they want to file the output back into the wiki

## Notes

- Marp slides require the Marp Slides plugin in Obsidian to preview
- Charts use matplotlib — ensure it's available in the Python environment
- All outputs include [[wikilinks]] back to source wiki articles
- Outputs can be filed back into the wiki to enhance it (Karpathy's "explorations add up" principle)
