# Installation Guide

Install the Karpathy-style LLM Knowledge Base system into your own Claude Code setup.

## Requirements

| Dependency | Version | Purpose |
|-----------|---------|---------|
| [Claude Code](https://claude.ai/claude-code) | Latest | LLM engine (skills, commands, agents, hooks) |
| [Obsidian](https://obsidian.md/) | 1.4+ | Wiki viewer and IDE frontend |
| [Python](https://www.python.org/) | 3.10+ | `kb_engine.py` script |
| [Node.js](https://nodejs.org/) | 18+ | Hook scripts |
| [Defuddle CLI](https://www.npmjs.com/package/defuddle-cli) | Latest | Web article extraction |

### Optional dependencies

| Dependency | Purpose | Install |
|-----------|---------|---------|
| [MarkItDown MCP](https://github.com/microsoft/markitdown) | PDF/DOCX/PPTX conversion | `uvx markitdown-mcp` or `pip install markitdown-mcp` |
| [Zotero MCP](https://github.com/pablodip/zotero-mcp) | Academic paper ingestion | `pip install zotero-mcp` + Zotero API key |
| [uv](https://docs.astral.sh/uv/) | Python package manager (needed for MarkItDown MCP) | `pip install uv` or via installer |
| [matplotlib](https://matplotlib.org/) | Chart generation in `/kb-output chart` | `pip install matplotlib` |

### Included skill dependency

| Skill | Purpose | Install |
|-------|---------|---------|
| `alphaxiv-paper-lookup` | Structured arXiv paper overviews via alphaxiv.org | Included (no extra install — uses `curl`) |

The `alphaxiv-paper-lookup` skill is bundled with the KB system. When `/kb-ingest` receives an arXiv URL, it automatically uses AlphaXiv's structured markdown overview instead of raw PDF extraction. It also works standalone for quick paper lookups outside of any KB context.

## Step 1: Install CLI dependencies

```bash
# Defuddle for web article extraction
npm install -g defuddle-cli

# Verify
defuddle --version
```

## Step 2: Copy the system files

All files go under your Claude Code home directory (`~/.claude/`). On Windows this is `C:\Users\<username>\.claude\`.

### Directory structure to create

```
~/.claude/
├── scripts/
│   └── kb_engine.py
├── skills/
│   ├── kb-wiki-authoring/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── ARTICLE-SCHEMA.md
│   │       ├── COMPILATION-PIPELINE.md
│   │       ├── MERGE-STRATEGY.md
│   │       └── INDEX-MAINTENANCE.md
│   ├── kb-source-ingestion/
│   │   └── SKILL.md
│   └── alphaxiv-paper-lookup/
│       └── SKILL.md
├── commands/
│   ├── kb-new.md
│   ├── kb-ingest.md
│   ├── kb-compile.md
│   ├── kb-query.md
│   ├── kb-lint.md
│   ├── kb-status.md
│   └── kb-output.md
├── agents/
│   ├── kb-compiler.md
│   ├── kb-query-agent.md
│   └── kb-linter.md
├── hooks/
│   └── kb-auto-compile-check.js
└── templates/
    └── kb-vault-template/
        ├── .obsidian/
        │   ├── app.json
        │   ├── core-plugins.json
        │   ├── community-plugins.json
        │   ├── graph.json
        │   └── plugins/
        │       ├── dataview/
        │       │   ├── manifest.json
        │       │   └── data.json
        │       └── marp-slides/
        │           └── manifest.json
        ├── raw/
        │   ├── web/
        │   ├── papers/
        │   ├── repos/
        │   └── notes/
        ├── wiki/
        │   ├── concepts/
        │   ├── sources/
        │   └── categories/
        ├── outputs/
        │   ├── reports/
        │   ├── slides/
        │   └── charts/
        └── _meta/
```

### Copy commands (from this repo)

If you cloned this repository, copy everything into place:

```bash
# Set your Claude Code home (adjust for your OS)
CLAUDE_HOME="$HOME/.claude"    # macOS/Linux
# CLAUDE_HOME="C:/Users/$USERNAME/.claude"  # Windows (Git Bash)

# Create directories
mkdir -p "$CLAUDE_HOME/scripts"
mkdir -p "$CLAUDE_HOME/skills/kb-wiki-authoring/references"
mkdir -p "$CLAUDE_HOME/skills/kb-source-ingestion"
mkdir -p "$CLAUDE_HOME/templates/kb-vault-template"

# Copy files (from the source-files/ directory in this repo)
cp source-files/scripts/kb_engine.py "$CLAUDE_HOME/scripts/"
cp source-files/skills/kb-wiki-authoring/SKILL.md "$CLAUDE_HOME/skills/kb-wiki-authoring/"
cp source-files/skills/kb-wiki-authoring/references/*.md "$CLAUDE_HOME/skills/kb-wiki-authoring/references/"
cp source-files/skills/kb-source-ingestion/SKILL.md "$CLAUDE_HOME/skills/kb-source-ingestion/"
cp source-files/commands/kb-*.md "$CLAUDE_HOME/commands/"
cp source-files/agents/kb-*.md "$CLAUDE_HOME/agents/"
cp source-files/hooks/kb-auto-compile-check.js "$CLAUDE_HOME/hooks/"
cp -r source-files/templates/kb-vault-template "$CLAUDE_HOME/templates/"
```

Or, if you're installing manually, create each file from the contents provided in the `source-files/` directory of this repository.

## Step 3: Configure the vault location

By default, knowledge base vaults are created at `D:\KnowledgeBases\`. To change this:

1. Open `~/.claude/scripts/kb_engine.py`
2. Find the line:
   ```python
   DEFAULT_KB_ROOT = Path("D:/KnowledgeBases")
   ```
3. Change it to your preferred location:
   ```python
   DEFAULT_KB_ROOT = Path.home() / "KnowledgeBases"        # ~/KnowledgeBases
   DEFAULT_KB_ROOT = Path("/data/knowledge-bases")          # Linux custom path
   DEFAULT_KB_ROOT = Path("C:/Users/you/KnowledgeBases")   # Windows custom path
   ```

## Step 4: Register the auto-compile hook

Add the PostToolUse hook to your `~/.claude/settings.json`. Open the file and add this entry inside the `"hooks"` object:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "node -e \"const{execSync}=require('child_process'),p=require('path'),h=require('os').homedir();execSync(\\\"node \\\"+p.join(h,'.claude/hooks/kb-auto-compile-check.js'),{stdio:'inherit'})\"",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

If you already have a `"hooks"` section, merge the `"PostToolUse"` array into it.

## Step 5: Configure MCP servers (optional)

### MarkItDown (PDF/DOCX/PPTX ingestion)

Add to `~/.claude/settings.json` under `"mcpServers"`:

**If you have `uv` installed (recommended):**
```json
"markitdown": {
  "command": "uvx",
  "args": ["markitdown-mcp"],
  "env": {}
}
```

**Windows with uv installed via WinGet:**
```json
"markitdown": {
  "command": "C:\\Users\\<username>\\AppData\\Local\\Microsoft\\WinGet\\Packages\\astral-sh.uv_Microsoft.Winget.Source_8wekyb3d8bbwe\\uvx.exe",
  "args": ["markitdown-mcp"],
  "env": {}
}
```

**Without uv (pip install):**
```bash
pip install markitdown-mcp
```
```json
"markitdown": {
  "command": "markitdown-mcp",
  "args": [],
  "env": {}
}
```

### Zotero (academic paper ingestion)

Requires a Zotero account and API key from https://www.zotero.org/settings/keys.

```bash
pip install zotero-mcp
```

Add to `~/.claude/settings.json` under `"mcpServers"`:
```json
"zotero": {
  "command": "zotero-mcp",
  "args": ["serve"],
  "env": {
    "ZOTERO_API_KEY": "your-api-key-here",
    "ZOTERO_LIBRARY_ID": "your-library-id",
    "ZOTERO_LIBRARY_TYPE": "user"
  }
}
```

## Step 6: Verify the installation

```bash
# Check kb_engine.py works
python ~/.claude/scripts/kb_engine.py list

# Should output: [] (empty list, no vaults yet)
```

Then in Claude Code, type:
```
/kb-new "Test Topic"
```

If the vault is created at your configured location, the installation is complete. You can delete the test vault afterwards:
```bash
rm -rf ~/KnowledgeBases/test-topic  # or wherever your vaults live
```

## Step 7: Install Obsidian plugins

When you open a new vault in Obsidian for the first time:

1. Obsidian will prompt "Trust author and enable plugins?" — click **Trust**
2. The vault comes pre-configured with:
   - **Dataview** — dynamic queries over wiki articles
   - **Marp Slides** — preview slide decks generated by `/kb-output slides`
3. Optionally install these community plugins from Obsidian's settings:
   - **Zotero Integration** — if you use Zotero for papers
   - **Omnisearch** — enhanced search across the vault

## Platform Notes

### macOS / Linux
- Paths use forward slashes: `~/.claude/scripts/kb_engine.py`
- `defuddle` and `node` should be on your PATH
- Python 3 may be `python3` instead of `python` — update command references in the `.md` files if needed

### Windows
- Paths use backslashes in settings.json but forward slashes work in Git Bash
- The hook scripts use Node.js — ensure `node` is on your PATH
- `kb_engine.py` uses `pathlib.Path` so it handles Windows paths correctly

## Uninstalling

Remove the KB system files:

```bash
CLAUDE_HOME="$HOME/.claude"

rm "$CLAUDE_HOME/scripts/kb_engine.py"
rm -rf "$CLAUDE_HOME/skills/kb-wiki-authoring"
rm -rf "$CLAUDE_HOME/skills/kb-source-ingestion"
rm "$CLAUDE_HOME/commands/kb-"*.md
rm "$CLAUDE_HOME/agents/kb-"*.md
rm "$CLAUDE_HOME/hooks/kb-auto-compile-check.js"
rm -rf "$CLAUDE_HOME/templates/kb-vault-template"
```

Remove the `PostToolUse` hook entry from `~/.claude/settings.json`.

Remove MCP server entries (`markitdown`, `zotero`) from settings.json if no longer needed.

Your knowledge base vaults are just Obsidian folders — they remain functional as plain markdown wikis even without the system installed.
