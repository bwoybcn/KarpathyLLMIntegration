#!/usr/bin/env python3
"""Deterministic operations engine for LLM Knowledge Base system.

Handles vault scaffolding, compilation state tracking, link validation,
index rebuilding, and statistics — all operations that don't require an LLM.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VAULT_MARKER = "_meta"
TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates" / "kb-vault-template"

RAW_SUBDIRS = ("web", "papers", "repos", "notes")
WIKI_SUBDIRS = ("concepts", "sources", "categories")
OUTPUT_SUBDIRS = ("reports", "slides", "charts")

WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

DEFAULT_KB_ROOT = Path("D:/KnowledgeBases")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def slugify(name: str) -> str:
    """Convert a topic name to a filesystem-safe slug."""
    slug = name.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = slug.strip("-")
    return slug


def file_hash(path: Path) -> str:
    """Compute SHA-256 hash of a file (first 12 hex chars)."""
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha.update(chunk)
    return sha.hexdigest()[:12]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def now_date() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def load_json(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def parse_frontmatter(text: str) -> dict[str, Any]:
    """Parse YAML-like frontmatter into a dict (simple key: value only)."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    result: dict[str, Any] = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if val.startswith("[") and val.endswith("]"):
                # Simple list parse
                items = val[1:-1].split(",")
                result[key] = [i.strip().strip('"').strip("'") for i in items if i.strip()]
            else:
                result[key] = val
    return result


# ---------------------------------------------------------------------------
# Vault detection
# ---------------------------------------------------------------------------

def detect_vault(start: Path) -> Optional[Path]:
    """Walk up from start to find a KB vault root (contains _meta/)."""
    current = start.resolve()
    for _ in range(20):
        if (current / VAULT_MARKER).is_dir() and (current / "raw").is_dir():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None


def find_all_vaults(root: Path = DEFAULT_KB_ROOT) -> list[Path]:
    """List all KB vaults under the root directory."""
    vaults = []
    if root.is_dir():
        for child in sorted(root.iterdir()):
            if child.is_dir() and (child / VAULT_MARKER).is_dir():
                vaults.append(child)
    return vaults


# ---------------------------------------------------------------------------
# Init — scaffold a new vault
# ---------------------------------------------------------------------------

def init_vault(topic: str, kb_root: Path = DEFAULT_KB_ROOT) -> Path:
    """Create a new KB vault from the template."""
    slug = slugify(topic)
    vault_path = kb_root / slug

    if vault_path.exists():
        print(f"ERROR: Vault already exists at {vault_path}", file=sys.stderr)
        sys.exit(1)

    # Copy template if it exists, otherwise scaffold manually
    if TEMPLATE_DIR.is_dir():
        shutil.copytree(TEMPLATE_DIR, vault_path)
    else:
        vault_path.mkdir(parents=True)

    # Ensure all directories exist
    for sub in RAW_SUBDIRS:
        (vault_path / "raw" / sub).mkdir(parents=True, exist_ok=True)
    for sub in WIKI_SUBDIRS:
        (vault_path / "wiki" / sub).mkdir(parents=True, exist_ok=True)
    for sub in OUTPUT_SUBDIRS:
        (vault_path / "outputs" / sub).mkdir(parents=True, exist_ok=True)
    (vault_path / VAULT_MARKER).mkdir(parents=True, exist_ok=True)
    (vault_path / ".obsidian" / "plugins").mkdir(parents=True, exist_ok=True)

    # Initialize compilation state
    state_path = vault_path / VAULT_MARKER / "compilation-state.json"
    if not state_path.exists():
        save_json(state_path, {
            "version": 1,
            "last_compiled": None,
            "sources": {},
            "wiki_articles": {},
        })

    # Initialize AGENTS.md
    agents_path = vault_path / "AGENTS.md"
    if not agents_path.exists():
        agents_path.write_text(
            f"# Knowledge Base: {topic}\n\n"
            "This is a Karpathy-style LLM knowledge base vault.\n\n"
            "## Structure\n"
            "- `raw/` — Source documents. Ingested via `/kb-ingest`.\n"
            "- `wiki/` — Compiled knowledge articles. LLM-authored via `/kb-compile`.\n"
            "- `outputs/` — Generated reports, slides, charts via `/kb-output`.\n"
            "- `_meta/` — Compilation state and indexes.\n\n"
            "## Rules\n"
            "- Always use `[[wikilinks]]` for cross-references within `wiki/`\n"
            "- Follow the article schema (see `kb-wiki-authoring` skill)\n"
            "- Never delete wiki articles — archive or merge instead\n"
            "- Update `_index.md` and `_categories.md` after any article changes\n"
            "- Attribute all claims to sources in the Evidence section\n"
            "- Use canonical concept name as filename (`kebab-case.md`)\n"
            "- Source summaries go in `wiki/sources/`, concepts in `wiki/concepts/`\n",
            encoding="utf-8",
        )

    # Initialize wiki index files
    for name, content in [
        ("wiki/_index.md", f"---\ntitle: Master Index\ntype: index\nupdated: {now_date()}\n---\n\n# {topic} — Master Index\n\n_No articles yet. Run `/kb-compile` after ingesting sources._\n"),
        ("wiki/_categories.md", f"---\ntitle: Categories\ntype: index\nupdated: {now_date()}\n---\n\n# Categories\n\n_No categories yet._\n"),
        ("wiki/_glossary.md", f"---\ntitle: Glossary\ntype: index\nupdated: {now_date()}\n---\n\n# Glossary\n\n_No terms yet._\n"),
        ("wiki/_backlinks.md", f"---\ntitle: Backlinks\ntype: index\nupdated: {now_date()}\n---\n\n# Backlinks Index\n\n_No backlinks yet._\n"),
    ]:
        p = vault_path / name
        if not p.exists():
            p.write_text(content, encoding="utf-8")

    # Initialize stats
    stats_path = vault_path / VAULT_MARKER / "stats.md"
    if not stats_path.exists():
        stats_path.write_text(
            f"# {topic} — Statistics\n\n"
            f"**Last updated**: {now_date()}\n\n"
            "| Metric | Value |\n"
            "|--------|-------|\n"
            "| Raw sources | 0 |\n"
            "| Wiki articles | 0 |\n"
            "| Total words | 0 |\n"
            "| Categories | 0 |\n"
            "| Uncompiled sources | 0 |\n"
            "| Broken links | 0 |\n",
            encoding="utf-8",
        )

    print(json.dumps({
        "status": "created",
        "vault_path": str(vault_path),
        "topic": topic,
        "slug": slug,
    }, indent=2))
    return vault_path


# ---------------------------------------------------------------------------
# Diff — find uncompiled raw sources
# ---------------------------------------------------------------------------

@dataclass
class DiffResult:
    new: list[str] = field(default_factory=list)
    modified: list[str] = field(default_factory=list)
    deleted: list[str] = field(default_factory=list)


def diff_sources(vault_path: Path) -> DiffResult:
    """Compare raw/ files against compilation-state.json."""
    state = load_json(vault_path / VAULT_MARKER / "compilation-state.json")
    compiled = state.get("sources", {})

    result = DiffResult()
    current_files: dict[str, str] = {}

    # Scan raw/ for all files
    raw_dir = vault_path / "raw"
    if raw_dir.is_dir():
        for f in raw_dir.rglob("*"):
            if f.is_file() and f.name != "_manifest.json":
                rel = f.relative_to(vault_path).as_posix()
                h = file_hash(f)
                current_files[rel] = h

                if rel not in compiled:
                    result.new.append(rel)
                elif compiled[rel].get("hash") != h:
                    result.modified.append(rel)

    # Check for deleted sources
    for rel in compiled:
        if rel not in current_files:
            result.deleted.append(rel)

    print(json.dumps({
        "new": result.new,
        "modified": result.modified,
        "deleted": result.deleted,
        "total_raw": len(current_files),
        "total_compiled": len(compiled),
    }, indent=2))
    return result


# ---------------------------------------------------------------------------
# Hash — update raw file hashes in compilation state
# ---------------------------------------------------------------------------

def hash_raw(vault_path: Path) -> None:
    """Update hashes for all raw files in compilation state."""
    state_path = vault_path / VAULT_MARKER / "compilation-state.json"
    state = load_json(state_path)
    sources = state.get("sources", {})

    raw_dir = vault_path / "raw"
    updated = 0
    if raw_dir.is_dir():
        for f in raw_dir.rglob("*"):
            if f.is_file() and f.name != "_manifest.json":
                rel = f.relative_to(vault_path).as_posix()
                h = file_hash(f)
                if rel not in sources:
                    sources[rel] = {}
                if sources[rel].get("hash") != h:
                    sources[rel]["hash"] = h
                    sources[rel]["compiled_at"] = now_iso()
                    updated += 1

    state["sources"] = sources
    state["last_compiled"] = now_iso()
    save_json(state_path, state)
    print(json.dumps({"updated": updated, "total": len(sources)}))


# ---------------------------------------------------------------------------
# Validate links — find broken [[wikilinks]]
# ---------------------------------------------------------------------------

def validate_links(vault_path: Path) -> list[dict]:
    """Find broken wikilinks in the wiki/ directory."""
    wiki_dir = vault_path / "wiki"
    if not wiki_dir.is_dir():
        print("[]")
        return []

    # Build set of all wiki files (by stem, lowercased)
    known_files: set[str] = set()
    for f in wiki_dir.rglob("*.md"):
        known_files.add(f.stem.lower())
        # Also add aliases from frontmatter
        text = f.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(text)
        for alias in fm.get("aliases", []):
            if isinstance(alias, str):
                known_files.add(slugify(alias))

    # Scan all wiki files for wikilinks
    broken: list[dict] = []
    for f in wiki_dir.rglob("*.md"):
        text = f.read_text(encoding="utf-8", errors="replace")
        rel = f.relative_to(vault_path).as_posix()
        for match in WIKILINK_RE.finditer(text):
            target = match.group(1).strip()
            target_slug = slugify(target)
            # Skip links to index files (they use special names)
            if target.startswith("_"):
                continue
            if target_slug not in known_files and target.lower() not in known_files:
                broken.append({
                    "file": rel,
                    "target": target,
                    "line": text[:match.start()].count("\n") + 1,
                })

    print(json.dumps(broken, indent=2))
    return broken


# ---------------------------------------------------------------------------
# Rebuild index — regenerate _index.md from article frontmatter
# ---------------------------------------------------------------------------

def rebuild_index(vault_path: Path) -> None:
    """Regenerate wiki/_index.md from all wiki articles."""
    wiki_dir = vault_path / "wiki"
    entries: list[dict] = []

    for subdir in ("concepts", "sources", "categories"):
        d = wiki_dir / subdir
        if not d.is_dir():
            continue
        for f in sorted(d.rglob("*.md")):
            text = f.read_text(encoding="utf-8", errors="replace")
            fm = parse_frontmatter(text)
            title = fm.get("title", f.stem.replace("-", " ").title())
            art_type = fm.get("type", subdir.rstrip("s"))
            # Extract first paragraph as summary
            body = FRONTMATTER_RE.sub("", text).strip()
            first_para = body.split("\n\n")[0] if body else ""
            # Clean markdown from summary
            summary = re.sub(r"[#*_\[\]]", "", first_para).strip()
            if len(summary) > 150:
                summary = summary[:147] + "..."

            rel = f.relative_to(wiki_dir).as_posix()
            entries.append({
                "title": title,
                "type": art_type,
                "path": rel,
                "summary": summary,
            })

    # Write _index.md
    topic = vault_path.name.replace("-", " ").title()
    lines = [
        "---",
        "title: Master Index",
        "type: index",
        f"updated: {now_date()}",
        "---",
        "",
        f"# {topic} — Master Index",
        "",
        f"**{len(entries)} articles**",
        "",
    ]

    # Group by type
    by_type: dict[str, list[dict]] = {}
    for e in entries:
        by_type.setdefault(e["type"], []).append(e)

    for art_type, items in sorted(by_type.items()):
        lines.append(f"## {art_type.title()}s")
        lines.append("")
        for item in items:
            link = f"[[{item['title']}]]"
            lines.append(f"- {link} — {item['summary']}")
        lines.append("")

    index_path = wiki_dir / "_index.md"
    index_path.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"articles": len(entries), "types": list(by_type.keys())}))


# ---------------------------------------------------------------------------
# Stats — generate _meta/stats.md
# ---------------------------------------------------------------------------

def compute_stats(vault_path: Path) -> dict:
    """Compute wiki statistics."""
    wiki_dir = vault_path / "wiki"
    raw_dir = vault_path / "raw"

    raw_count = sum(1 for f in raw_dir.rglob("*") if f.is_file() and f.name != "_manifest.json") if raw_dir.is_dir() else 0

    article_count = 0
    total_words = 0
    categories: set[str] = set()
    concepts = 0
    source_summaries = 0

    if wiki_dir.is_dir():
        for f in wiki_dir.rglob("*.md"):
            if f.name.startswith("_"):
                continue
            article_count += 1
            text = f.read_text(encoding="utf-8", errors="replace")
            total_words += len(text.split())
            fm = parse_frontmatter(text)
            if fm.get("type") == "concept":
                concepts += 1
            elif fm.get("type") == "source-summary":
                source_summaries += 1
            cat = fm.get("category", "")
            if cat:
                categories.add(cat.strip("[]\"'"))

    # Check compilation state for uncompiled
    state = load_json(vault_path / VAULT_MARKER / "compilation-state.json")
    compiled_sources = set(state.get("sources", {}).keys())
    current_raw: set[str] = set()
    if raw_dir.is_dir():
        for f in raw_dir.rglob("*"):
            if f.is_file() and f.name != "_manifest.json":
                current_raw.add(f.relative_to(vault_path).as_posix())
    uncompiled = len(current_raw - compiled_sources)

    # Broken links
    broken_links = len(validate_links.__wrapped__(vault_path)) if hasattr(validate_links, '__wrapped__') else 0

    stats = {
        "raw_sources": raw_count,
        "wiki_articles": article_count,
        "concepts": concepts,
        "source_summaries": source_summaries,
        "total_words": total_words,
        "categories": len(categories),
        "uncompiled_sources": uncompiled,
    }

    # Write stats.md
    topic = vault_path.name.replace("-", " ").title()
    stats_md = (
        f"# {topic} — Statistics\n\n"
        f"**Last updated**: {now_date()}\n\n"
        "| Metric | Value |\n"
        "|--------|-------|\n"
        f"| Raw sources | {raw_count} |\n"
        f"| Wiki articles | {article_count} |\n"
        f"| Concepts | {concepts} |\n"
        f"| Source summaries | {source_summaries} |\n"
        f"| Total words | {total_words:,} |\n"
        f"| Categories | {len(categories)} |\n"
        f"| Uncompiled sources | {uncompiled} |\n"
    )
    (vault_path / VAULT_MARKER / "stats.md").write_text(stats_md, encoding="utf-8")

    print(json.dumps(stats, indent=2))
    return stats


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="LLM Knowledge Base engine — deterministic operations",
        prog="kb_engine",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # init
    p_init = sub.add_parser("init", help="Create a new KB vault from template")
    p_init.add_argument("--topic", required=True, help="Topic name for the vault")
    p_init.add_argument("--kb-root", type=Path, default=DEFAULT_KB_ROOT,
                        help=f"Root directory for KB vaults (default: {DEFAULT_KB_ROOT})")

    # diff
    p_diff = sub.add_parser("diff", help="Find uncompiled raw sources")
    p_diff.add_argument("--vault-path", type=Path, help="Vault path (auto-detected from CWD if omitted)")

    # hash-raw
    p_hash = sub.add_parser("hash-raw", help="Update raw file hashes in compilation state")
    p_hash.add_argument("--vault-path", type=Path, help="Vault path")

    # validate-links
    p_links = sub.add_parser("validate-links", help="Find broken wikilinks")
    p_links.add_argument("--vault-path", type=Path, help="Vault path")

    # rebuild-index
    p_index = sub.add_parser("rebuild-index", help="Regenerate _index.md")
    p_index.add_argument("--vault-path", type=Path, help="Vault path")

    # stats
    p_stats = sub.add_parser("stats", help="Compute and write wiki statistics")
    p_stats.add_argument("--vault-path", type=Path, help="Vault path")

    # detect
    p_detect = sub.add_parser("detect", help="Detect if CWD is inside a KB vault")
    p_detect.add_argument("--cwd", type=Path, default=Path.cwd(), help="Directory to check")

    # list
    p_list = sub.add_parser("list", help="List all KB vaults")
    p_list.add_argument("--kb-root", type=Path, default=DEFAULT_KB_ROOT)

    args = parser.parse_args()

    # Resolve vault path for commands that need it
    vault_path: Optional[Path] = None
    if hasattr(args, "vault_path") and args.vault_path:
        vault_path = args.vault_path.resolve()
    elif args.command not in ("init", "detect", "list"):
        vault_path = detect_vault(Path.cwd())
        if not vault_path:
            print("ERROR: Not inside a KB vault. Use --vault-path or cd into a vault.", file=sys.stderr)
            sys.exit(1)

    if args.command == "init":
        init_vault(args.topic, args.kb_root)
    elif args.command == "diff":
        diff_sources(vault_path)
    elif args.command == "hash-raw":
        hash_raw(vault_path)
    elif args.command == "validate-links":
        validate_links(vault_path)
    elif args.command == "rebuild-index":
        rebuild_index(vault_path)
    elif args.command == "stats":
        compute_stats(vault_path)
    elif args.command == "detect":
        result = detect_vault(args.cwd)
        if result:
            print(json.dumps({"vault_path": str(result), "topic": result.name}))
        else:
            print(json.dumps({"vault_path": None}))
    elif args.command == "list":
        vaults = find_all_vaults(args.kb_root)
        print(json.dumps([{"path": str(v), "topic": v.name} for v in vaults], indent=2))


if __name__ == "__main__":
    main()
