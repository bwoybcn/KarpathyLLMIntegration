---
name: kb-query
description: Ask a question against a Knowledge Base wiki and get a researched answer with citations
args:
  - name: question
    description: The question to research and answer
    required: true
  - name: vault
    description: Vault name or path. Auto-detected from CWD if omitted.
    required: false
  - name: save
    description: Save the answer to outputs/reports/. Default false.
    required: false
    default: "false"
tags: [Knowledge Base, Q&A, Research]
---

# /kb-query — Ask a Question Against the Wiki

Research and answer a question using the compiled knowledge base wiki.

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

5. **Optionally save** (if `$save` is "true" or user requests):
   - Save to `outputs/reports/{question-slug}.md`
   - Add frontmatter with the question, date, and sources consulted
   - Ask if the user wants to file key findings back into the wiki

## Notes

- The agent reads the index first, then selectively reads full articles — it doesn't need to read the entire wiki
- For questions the wiki can't answer, the agent can optionally search the web
- Answers are attributed to specific wiki articles via wikilinks
