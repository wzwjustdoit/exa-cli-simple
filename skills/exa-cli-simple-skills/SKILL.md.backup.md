---
name: exa-cli-simple
description: >
  CLI tool that wraps Exa's WebSearch and WebFetch APIs.
  Trigger when the user needs to search the web, find up-to-date information,
  fetch page content from URLs, or verify facts with live data.
  Suitable for answering questions that require current/realtime information,
  or batch-fetching readable content from multiple URLs.
---

# exa-cli-simple Skill

This skill provides access to the Exa search engine via the terminal-based
`exa-cli-simple` CLI tool.

## When to Use

- User needs to **search the web** for current information (news, docs,
  people, companies)
- User needs to **fetch readable content** from one or more URLs
- User needs to **look up real-time or factual information** on a specific topic
- User needs to **verify or supplement** knowledge not in the training data
- Good as an alternative to built-in web_search / web_fetch for cleaner,
  more structured results

## Prerequisites

- `exa-cli-simple` installed:
  `pip install exa-cli-simple` or `uv tool install exa-cli-simple`
- `EXA_API_KEY` environment variable set (or pass `--api-key` each time)

## Commands

### 1. `exa search <query>` — Search the Web

```bash
exa search "<query>" [options]
```

Performs semantic search. Describe the ideal page, not keywords.

**Query tips**:
- ✅ `"blog post comparing React and Vue performance 2025"`
- ❌ `"React vs Vue"`

**Options**:

| Option | Description | Default |
|---|---|---|
| `-n <N>` | Number of results | 10 |
| `--json` | Output as JSON | off |
| `--pretty` | Pretty-print JSON (use with --json) | off |

**Examples**:
```bash
# Default text output
exa search "how to use exa python sdk?"

# JSON output for programmatic use
exa search "latest AI news 2026" -n 5 --json

# Pretty-printed JSON
exa search "best practices for CLI tools" --json --pretty

# Limit result count
exa search "category:company OpenAI funding" -n 3
```

### 2. `exa fetch <url> [<url>...]` — Fetch Page Content

```bash
exa fetch <url> [<url>...] [options]
```

Fetches clean readable text from one or more URLs.

**Options**:

| Option | Description | Default |
|---|---|---|
| `-m <N>` | Max characters per page | unlimited |
| `--json` | Output as JSON | off |
| `--pretty` | Pretty-print JSON (use with --json) | off |

**Examples**:
```bash
# Single URL
exa fetch "https://exa.ai/docs"

# Multiple URLs
exa fetch "https://exa.ai/docs" "https://exa.ai/blog"

# Truncate long content
exa fetch "https://example.com/long-article" -m 2000

# JSON output
exa fetch "https://exa.ai" --json
```

## Structured Data in Agent Workflows

Always use `--json` when results need further processing:

```bash
# Search, get JSON, pipe into jq or Python
exa search "python async patterns" -n 5 --json | jq
```

## Best Practices

1. **Search first, fetch second**: Start with `exa search` to discover relevant
   pages. If highlights are insufficient, follow up with `exa fetch` on
   specific URLs.
2. **Semantic queries**: Exa uses semantic understanding — describe the kind
   of page you want rather than listing keywords.
3. **Right-size results**: Default 10 results is usually good; adjust with `-n`
   for wider or narrower result sets.
4. **Use JSON for automation**: Always use `--json` when the output feeds into
   further tooling or code.
5. **Batch URLs**: `exa fetch` accepts multiple URLs in one call — batch them
   to save round-trips.
6. **Truncate when needed**: Use `-m` to limit fetch output when you only
   need a preview.

## Notes

- API key can be set via `--api-key <KEY>` or the `EXA_API_KEY` environment
  variable.
- Search is **semantic, not keyword-based** — describe the content type
  you are looking for.
- Use `category:people` or `category:company` to scope searches to LinkedIn
  profiles or company pages.
- `exa search` results include highlights (snippets). For full content, use
  `exa fetch` on the specific URL.
