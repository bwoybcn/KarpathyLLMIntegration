---
title: Dashboards
type: index
---

# Knowledge Base Dashboards

Live views powered by Dataview. These update automatically as the wiki grows.

---

## Articles by Type

```dataview
TABLE type, confidence, length(sources) as "Sources"
FROM "wiki/concepts" OR "wiki/sources" OR "wiki/categories"
WHERE type
SORT type ASC, title ASC
```

## High Confidence Concepts

```dataview
LIST
FROM "wiki/concepts"
WHERE confidence = "high"
SORT title ASC
```

## Low Confidence — Needs More Sources

```dataview
TABLE confidence, length(sources) as "Sources"
FROM "wiki/concepts"
WHERE confidence = "low" OR confidence = "medium"
SORT confidence ASC, title ASC
```

## Recently Updated (Last 7 Days)

```dataview
TABLE updated, type
FROM "wiki"
WHERE updated >= date(today) - dur(7 days)
SORT updated DESC
```

## Articles With Fewest Sources

```dataview
TABLE length(sources) as "Sources", confidence
FROM "wiki/concepts"
WHERE sources
SORT length(sources) ASC
LIMIT 10
```

## Source Summaries by Type

```dataview
TABLE source_type, author, date_published
FROM "wiki/sources"
SORT source_type ASC, date_published DESC
```

## All Tags

```dataview
LIST
FROM "wiki"
FLATTEN tags as tag
GROUP BY tag
SORT key ASC
```
