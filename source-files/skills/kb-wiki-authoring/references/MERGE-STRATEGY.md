# Merge Strategy Reference

## When Merging Is Needed

A merge happens when a new raw source discusses a concept that already has a `wiki/concepts/{slug}.md` article. The goal is to enrich the existing article with new information without losing anything.

## Merge Rules

### Rule 1: Never Delete

Never remove existing content during a merge. Information can be:
- Reorganized (moved to a more appropriate section)
- Annotated (marked as potentially outdated or contradicted)
- Expanded (new details added alongside existing)

But never deleted.

### Rule 2: Attribute Everything

Every new claim added must be attributed to its source in the Evidence section:
```markdown
## Evidence and Sources
- From [[Source: Existing Article]]: original finding
- From [[Source: New Article]]: new supporting or contrasting data   ← NEW
```

### Rule 3: Handle Contradictions

If the new source contradicts an existing claim:
- Keep BOTH claims with their respective attributions
- Add a note in `## Open Questions` about the disagreement
- Adjust `confidence` if warranted (e.g., high → medium)

```markdown
## Evidence and Sources
- From [[Source: Paper A]]: "X performs 20% better than Y"
- From [[Source: Paper B]]: "No significant difference between X and Y" (contradicts Paper A; different evaluation methodology)

## Open Questions
- Conflicting results on X vs Y performance — may depend on evaluation setup
```

### Rule 4: Expand, Don't Duplicate

If the new source covers the same ground as existing content:
- Strengthen existing points with additional evidence
- Add nuance or detail that was missing
- Don't repeat the same information in different words

### Rule 5: Update Metadata

After merging, update:
- `updated` date in frontmatter
- `sources` list — add the new raw source path
- `tags` — add any new relevant tags
- `aliases` — add any new name variants encountered
- `confidence` — adjust based on strength of combined evidence

## Merge Procedure

1. Read the existing concept article in full
2. Read the new source material (the specific parts about this concept)
3. Identify what's genuinely new:
   - New claims not already covered
   - New evidence for existing claims
   - New relationships to other concepts
   - Contradictions with existing claims
4. Write the merged article:
   - Keep the existing structure and all content
   - Add new information to the appropriate sections
   - Add new source attributions
   - Add new wikilinks
   - Update frontmatter
5. Verify the merged article:
   - All existing wikilinks still present
   - All new claims are attributed
   - Frontmatter is complete and correct
   - No duplicate paragraphs or redundant sections
