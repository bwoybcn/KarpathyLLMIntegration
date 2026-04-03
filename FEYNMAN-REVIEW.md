# Feynman Review: LLM Knowledge Base System

A deep critical review of the entire project using the Feynman Thinking Framework.

---

## ORIENT

```
Thinking task:     Proposal stress-test + Understanding deepening
Mode:              2 (Deep) — high-stakes review of a complete system before sharing publicly
Primary strategies: Creation Test, Intellectual Honesty, Multiple Representations
Goal:              Identify genuine weaknesses, illusions of completeness, and the gap
                   between what we think we built and what we actually built
```

---

## DEFINE

```
Plain statement:   We built a system where you type commands in Claude Code, and an LLM
                   finds sources, converts them to markdown, writes wiki articles with
                   cross-references, and puts them in an Obsidian vault you can browse.
                   It has 9 commands, 4 agents, 3 skills, 1 hook, 1 Python script, and
                   a pre-configured vault template.

Claims:
  - The system can autonomously research, ingest, compile, query, lint, and expand a KB
  - It works for academic research, news stories, and general topics
  - It produces Obsidian-native output (callouts, Dataview, canvas, structured tags, embeds)
  - Other people can install it from the GitHub repo
  - The wiki grows and improves over time through the lint -> expand loop

Open questions:
  - Has any of this actually been tested end-to-end with real data?
  - Do the agents actually produce quality output, or do they just have good instructions?
  - Would a non-expert actually succeed at installing and using this?

Core tension:      This is a system of INSTRUCTIONS (skills, commands, agent prompts) not
                   a system of CODE. The Python script handles state, but the actual
                   intelligence -- compilation, merging, research -- is entirely dependent
                   on the LLM following the instructions well. We've built a recipe, not
                   a machine.

Label alerts:
  - "Autonomous research" -- actually means "the LLM runs WebSearch and we hope it
    picks good sources"
  - "Incremental compilation" -- actually means "the LLM reads old + new and rewrites,
    hopefully preserving everything"
  - "Quality tiers" -- instructions to the LLM, not enforced filters
```

---

## DECOMPOSE

```
Premises:
  1. Claude Code agents reliably follow long prompt instructions
     -- UNCERTAIN (agents can drift, skip steps, or hallucinate structure)

  2. WebSearch returns relevant results for arbitrary topics
     -- PARTIALLY VERIFIED (works for well-known topics, unreliable for niche or recent)

  3. Defuddle successfully extracts clean content from most websites
     -- PARTIALLY VERIFIED (fails on JS-heavy sites, paywalls, some layouts)

  4. The merge strategy (read existing + new, rewrite preserving all) works at scale
     -- UNVERIFIED (never tested with 50+ articles)

  5. Dataview queries work with our frontmatter format
     -- LIKELY BUT UNVERIFIED (inline YAML lists may not parse as Dataview expects)

  6. The canvas generation step actually produces valid .canvas JSON
     -- UNVERIFIED (the compile command tells the agent to generate it, but there's
     no script or template for the JSON structure)

  7. Other Claude Code users have the same tool access (WebSearch, WebFetch)
     -- UNCERTAIN (depends on their plan and configuration)

  8. The hook protocol format is correct
     -- UNCERTAIN (we changed to JSON output but haven't tested if Claude Code
     actually reads it that way)

Cargo Cult alerts:
  - The Obsidian plugin configs (dataview/manifest.json, marp-slides/manifest.json)
    ship without main.js -- Obsidian will NOT load these plugins. The manifest is form
    without function. Users must install plugins manually via the community browser,
    which INSTALL.md now correctly states, but the template files create a false
    impression of "pre-configured."

Verified fundamentals:
  - kb_engine.py works (tested: init, diff, stats, detect, list, validate-links)
  - The vault directory structure is sound and creates correctly
  - Wikilinks are well-defined and the schema is consistent
  - The command/skill/agent/hook file formats match existing infrastructure
```

---

## EXPLAIN

```
Simple explanation:
  You drop sources into a folder. You tell the AI to process them. It reads each source,
  figures out what concepts are in it, and writes wiki pages about those concepts --
  linking them together with [[wikilinks]]. If a concept already has a page, it adds the
  new information to the existing page. Over time you build up a connected web of
  knowledge you can browse in Obsidian, ask questions against, and generate reports from.

  The AI can also go find sources for you (web search), check the wiki for problems
  (linting), and automatically fill gaps it finds (expand).

Gaps identified:
  - MERGE QUALITY: The hardest part of the system -- merging new information into
    existing articles without losing content or creating duplicates -- is entirely LLM
    judgment. There's no diff, no version control, no undo. If the LLM botches a merge,
    content is silently lost. This is the single biggest risk.

  - CANVAS GENERATION: The compile command says "generate a canvas" but there's no code
    or detailed spec for producing valid JSON Canvas format. The agent would need to know
    the exact node/edge schema. This will likely fail on first use.

  - END-TO-END TESTING: Zero real-world testing. Every component was built and reviewed
    in isolation. We don't know if the full pipeline (research -> ingest -> compile ->
    query) actually produces a coherent wiki.

  - DATAVIEW COMPATIBILITY: The dashboard queries assume Dataview can read our frontmatter
    fields. If inline YAML lists like sources: ["a", "b"] aren't parsed as arrays by
    Dataview, most queries will return empty results.

Creation Test:     PARTIAL -- the deterministic parts (kb_engine.py, vault structure, file
                   formats) could be recreated from understanding. The agent behavior
                   (compile quality, merge quality, research quality) cannot be predicted
                   without testing.

Understanding level: 3 (Mechanistic) -- we understand the process and causal chain, but
                     haven't reached Level 4 (Generative) because we can't yet predict
                     how it behaves with real data.
```

---

## CHALLENGE

```
Steel-man objections:

  1. "This is a prompt collection, not a product."
     The actual intelligence is Claude following instructions. If Claude is having a bad
     day, misreads the schema, or doesn't follow the merge rules, the wiki degrades
     silently. There's no validation layer between the LLM's output and the wiki.
     kb_engine.py validates links but not content quality.

  2. "The merge problem is unsolved."
     Karpathy himself said this is a 'hacky collection of scripts.' Incremental merge
     of knowledge articles is a research-level problem. Telling an LLM 'preserve all
     existing content and add new' is an instruction, not a guarantee. At 100+ articles,
     merge drift will accumulate.

  3. "The installation barrier is too high for the claimed audience."
     The INSTALL.md requires: Claude Code, Obsidian, Python 3.10+, Node.js 18+, npm,
     defuddle-cli, optionally uv, MarkItDown MCP, Zotero MCP. Then copying ~30 files
     into the right directories and editing settings.json. The manual targets 'intelligent
     but non-expert' users but the install process requires developer comfort.

Self-deception risk: MODERATE -- we've been building and reviewing in a tight loop for
  hours. The code reviews found real bugs, but they reviewed code correctness, not
  behavioral correctness. We may be confusing 'well-structured instructions' with
  'working system.'

Falsifiability:    Falsifiable -- create a vault, ingest 5 sources, compile, and check
                   if the wiki is coherent, wikilinks resolve, and the dashboard works.
                   This is the obvious test we haven't run.

Authority check:   FLAGGED -- the entire project is inspired by Karpathy's tweet. We're
                   building toward his vision, but his system is custom scripts he's
                   iterated on. We don't know if our prompt-based approach replicates
                   the quality of a custom-scripted approach.
```

---

## REFRAME

```
Framing 1 (Adversarial):
  A skeptic would say: "You spent hours writing instructions for an AI to follow,
  then reviewed those instructions twice, then wrote documentation about those
  instructions, then made a PDF manual about those instructions. At no point did
  you actually RUN the system on real data. This is architecture astronautics --
  beautiful blueprints for a building no one has entered."

Framing 2 (Temporal):
  In 6 months, Claude will be better at following complex instructions, Obsidian
  may have native AI features, and someone may have built a proper product for this
  (Karpathy said "there is room for an incredible new product"). The value of this
  project is as a WORKING PROTOTYPE that validates the workflow -- but only if it
  actually works. Right now it's a validated architecture, not a validated system.

Framing 3 (Stakeholder -- the GitHub visitor):
  Someone finds this repo. They see a polished README, a nice manual, and 30+ files.
  They spend 30 minutes installing. They run /kb-new and /kb-research. If it works
  well, they're delighted. If the compile step produces mangled articles or the
  dashboard shows nothing, they close the tab and never come back. First impression
  is everything, and we have zero confidence in the first impression.

Surprising connection:
  The adversarial framing is uncomfortably accurate. We've optimized for REVIEWABILITY
  (clean code, good docs, consistent structure) but not for USABILITY (does it actually
  produce good output?). These are different things.
```

---

## SYNTHESIZE

```
Refined understanding:
  We built a well-architected, thoroughly documented system of LLM instructions that
  SHOULD produce a Karpathy-style knowledge base. The architecture is sound, the code
  (kb_engine.py) works, the file formats are consistent, the Obsidian integration is
  deep, and the docs are comprehensive.

  BUT: we have never run it end-to-end. The core value proposition -- "the LLM compiles
  raw sources into a good wiki" -- is untested. The merge strategy, research quality,
  callout formatting, Dataview compatibility, and canvas generation are all theoretical.

Honest gaps:
  - End-to-end test with real data        -- MATTERS (must do before claiming it works)
  - Merge quality at scale (50+ articles) -- MANAGEABLE (test with 10 first, iterate)
  - Canvas JSON generation                -- MATTERS (likely to fail without a concrete spec)
  - Dataview frontmatter compatibility    -- MATTERS (easy to test, easy to fix)
  - Installation complexity for non-experts-- IRREDUCIBLE (this is a power-user tool)
  - Hook protocol correctness             -- MANAGEABLE (test once, confirm or fix)

Next moves:
  1. RUN IT. Create a real vault, research a real topic, compile, and see what comes
     out. This is the single highest-value next step.
  2. Test Dataview compatibility -- open a compiled vault in Obsidian and check if the
     dashboard queries return results.
  3. Fix or spec the canvas generation -- either add concrete JSON Canvas format to
     the compile command, or remove the claim until it's implemented.
  4. After testing, iterate on whatever breaks -- which will certainly be something.
```

---

## Bottom Line

The architecture is solid and the documentation is excellent. But we've built a car, polished it, written the owner's manual, and never turned the key. The single most important thing to do next is **run `/kb-new` + `/kb-research` + `/kb-compile` on a real topic** and see what actually comes out.
