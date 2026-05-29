---
name: exa-cli-simple-skills
description: >-
  Use this skill whenever the user wants to search the web, fetch web page
  content, look up information online, retrieve URLs, do web research, or
  query the internet. This skill wraps the Exa API via the `exa` CLI tool
  (exa-cli-simple). Triggers include: "search the web for X", "look up X
  online", "fetch this URL", "get the contents of this page", "research X",
  "find information about X on the internet", or any request that requires
  real-time web data. Always use this skill for web search and web fetch
  tasks — even if the user doesn't explicitly mention Exa or the CLI.
---

# Exa CLI Simple

A CLI tool for web search and web page content fetching via the Exa API.

## Prerequisites

- The `exa` CLI must be installed: `pip install exa-cli-simple` or `uv tool install exa-cli-simple`
- An Exa API key is required, set via `EXA_API_KEY` environment variable or passed with `--api-key`

## Commands

### Search the web

```bash
exa search "<query>" [-n NUM_RESULTS] [--json] [--pretty]
```

- `query`: Describe the ideal page you want, not just keywords. For example, "articles about Python async patterns" rather than "python async".
- `-n`, `--num-results`: Number of results (default: 10)
- `--json`, `-j`: Output as JSON instead of human-readable text
- `--pretty`, `-p`: Pretty-print JSON (use with `--json`)

Human-readable output includes: title, URL, score, published date, and up to 3 highlights per result.

### Fetch page content

```bash
exa fetch <url> [url...] [-m MAX_CHARACTERS] [--json] [--pretty]
```

- `urls`: One or more URLs to fetch (required, at least one)
- `-m`, `--max-characters`: Truncate text to this many characters per page (default: no limit)
- `--json`, `-j`: Output as JSON instead of human-readable text
- `--pretty`, `-p`: Pretty-print JSON (use with `--json`)

When `--max-characters` is set and text exceeds the limit, output ends with `...[truncated]`.

### Common options (both commands)

- `--api-key`: Exa API key (falls back to `EXA_API_KEY` env var)
- `--json`, `-j`: Output in JSON format
- `--pretty`, `-p`: Pretty-print JSON output

## Behavior notes

- All output is UTF-8 encoded
- Errors are printed to stderr; when `--json` is used, errors are also JSON-formatted (`{"error": "..."}`)
- Empty/blank queries and URLs cause an immediate error exit
- The JSON output for search results is an array of result objects; for fetch results, an array of page content objects

## Common patterns

**Quick research lookup:**
```bash
exa search "best practices for Docker multi-stage builds"
```

**Get structured data for further processing:**
```bash
exa search "Rust async runtime comparison" --json --pretty
```

**Fetch and read a specific page:**
```bash
exa fetch https://example.com/article -m 5000
```

**Fetch multiple pages at once:**
```bash
exa fetch https://example.com/page1 https://example.com/page2 --json
```

## When to prefer search vs fetch

- Use **search** when the user asks a question, wants to discover relevant pages, or needs to find information on a topic
- Use **fetch** when the user provides specific URLs, wants to read a known page, or needs the full text content of particular documents
- If unsure which to use, prefer **search** first, then follow up with **fetch** on the most relevant result URLs
