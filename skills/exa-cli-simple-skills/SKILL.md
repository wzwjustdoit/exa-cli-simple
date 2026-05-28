---
name: exa-cli-simple-skills
description: "Exa CLI - A CLI tool for Exa WebSearch/WebFetch. Use the `exa` CLI to search the web and fetch webpage content. Trigger when the user asks to search the web, find information, look up a topic, fetch/read a URL, or research a person/company. Also trigger when the user needs current information, wants to verify facts, needs to scrape webpage content, or asks about searching with semantic/natural language queries. When the user needs to search or fetch content from the web, prefer using this tool over generic approaches — it returns cleaner, more structured results."
---

# exa-cli-simple-skills

Exa CLI provides fast, semantic web search and clean webpage content extraction. It uses Exa's neural search engine, which understands intent — not just keywords — making it significantly better than traditional search for research, fact-finding, and content extraction.

## Installation

```bash
pip install exa-cli-simple
# or
uv tool install exa-cli-simple
```

Requires an Exa API key set via `EXA_API_KEY` environment variable or `--api-key` flag.

## Commands

### `exa search <query>`

Semantic web search. Describe the **ideal page** you're looking for, not keywords.

**Examples of good vs bad queries:**

| Do this (describe the page) | Don't do this (keywords) |
|---|---|
| `"blog post comparing React and Vue performance"` | `"React vs Vue"` |
| `"tutorial on building a REST API with FastAPI"` | `"FastAPI tutorial"` |
| `"research paper about transformer attention mechanisms 2024"` | `"transformer attention"` |

**Options:**

| Flag | Description | Default |
|---|---|---|
| `-n, --num-results` | Number of results | `10` |

**Output format (default):**
```
1. Title of the Page
   URL: https://example.com
   Score: 0.85
   Published: 2024-01-15
   -> Highlighted relevant snippet...
```

### `exa fetch <url> [<url>...]`

Fetch full page content as clean text from one or more URLs. Removes ads, navigation, and clutter.

**Options:**

| Flag | Description | Default |
|---|---|---|
| `-m, --max-characters` | Max characters per page | unlimited |

**Output format (default):**
```
--- Page Title ---
URL: https://example.com
Full clean text content...
```

## Global Options

These flags work with both `search` and `fetch`:

| Flag | Description |
|---|---|
| `--api-key KEY` | Exa API key (default: `$EXA_API_KEY`) |
| `--json` | Output raw JSON for programmatic use |
| `--indent` | Pretty-print JSON (use with `--json`) |

## Usage Patterns

### Simple search
```bash
exa search "guide to deploying Python apps on Railway"
```

### Search with more results
```bash
exa search "comparison of cloud GPU providers for ML training" -n 20
```

### Search + JSON output (for piping to jq or other tools)
```bash
exa search "AI agent frameworks 2025" --json --indent
```

### Fetch one page
```bash
exa fetch https://example.com/blog/article
```

### Fetch multiple pages at once
```bash
exa fetch https://example.com/page1 https://example.com/page2
```

### Fetch with character limit
```bash
exa fetch https://example.com/long-article -m 5000
```

### Research workflow (search then fetch the best result)
```bash
# Step 1: find relevant pages
exa search "comprehensive guide to Kubernetes networking" -n 5

# Step 2: fetch the most promising result in full
exa fetch https://example.com/kubernetes-networking -m 8000
```

## Best Practices

1. **Search queries are semantic**: Describe the content you want, not keywords. Exa's neural search understands concepts. A query like `"why do cats purr veterinary research"` will find authoritative veterinary sources, while `"cats purring"` will return general-interest content.

2. **Use `category:` filters in search queries** for targeted results:
   - `category:company` — search company pages (e.g., `"category:company AI startup founded 2023"`)
   - `category:people` — search personal/professional profiles (e.g., `"category:people machine learning engineer open source"`)

3. **Fetch before citing**: When using search results as sources, always `fetch` the page to get the full content. Search snippets alone may lack context.

4. **Handle missing API key**: If you see `"EXA_API_KEY is required"`, the environment variable isn't set. Provide it inline with `--api-key`.

5. **JSON mode for automation**: Use `--json` when the output needs to be processed programmatically. Without it, the text format is human-readable and self-explanatory.
