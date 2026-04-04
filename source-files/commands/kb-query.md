---
name: kb-query
description: Ask a question against a Knowledge Base wiki and get a researched answer with citations. Answers are always saved to the vault.
args:
  - name: question
    description: The question to research and answer
    required: true
  - name: vault
    description: Vault name or path. Auto-detected from CWD if omitted.
    required: false
tags: [Knowledge Base, Q&A, Research]
---

# /kb-query — Ask a Question Against the Wiki

Research and answer a question using the compiled knowledge base wiki. Answers are always saved to the vault so explorations add up over time.

## Workflow

1. **Detect the target vault**:
   - If `$vault` is provided, resolve it
   - Otherwise, run: `python "$HOME/.claude/scripts/kb_engine.py" detect --cwd "$PWD"`

2. **Check wiki status**:
   - Run: `python "$HOME/.claude/scripts/kb_engine.py" stats --vault-path "<vault>"`
   - If wiki has 0 articles, tell the user to compile first

3. **Delegate to kb-query-agent**:
   - Pass the question and vault path
   - The agent will:
     a. Read `wiki/_index.md` and `wiki/_glossary.md`
     b. Identify and read relevant articles
     c. Synthesize an answer with `[[wikilink]]` citations
     d. Note gaps in the wiki's coverage

4. **Present the answer** to the user with citations.

5. **Always save the answer** to the vault:
   - Save to `outputs/reports/{question-slug}.md`
   - Include frontmatter:
     ```yaml
     ---
     title: "Q: {question}"
     type: query-report
     created: {today}
     question: "{question}"
     sources_consulted: [list of wiki articles read]
     tags: [type/query, topic/{relevant topic}]
     ---
     ```
   - The saved report includes the full answer, citations, identified gaps, and suggested follow-ups
   - These reports are browsable in Obsidian under `outputs/reports/`
   - They feed into future `/kb-expand` cycles — gaps identified in queries become research targets

## Notes

- The agent reads the index first, then selectively reads full articles — it doesn't need to read the entire wiki
- For questions the wiki can't answer, the agent can optionally search the web
- Answers are attributed to specific wiki articles via wikilinks
- Every query enriches the vault — this is Karpathy's "explorations add up" principle
