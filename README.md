# About: exa-cli-simple

Exa CLI - A CLI tool for Exa WebSearch/WebFetch

## Installation

```bash
pip install exa-cli-simple
# or
uv tool install exa-cli-simple
```

## Usage

```bash
export EXA_API_KEY=your_key_here
exa search "blog post about AI agents"
exa fetch https://example.com
```

## Commands

### `exa search <query>`

Search the web. Describe the ideal page, not keywords.

| Option | Description | Default |
|---|---|---|
| `-n, --num-results` | Number of results | `10` |

### `exa fetch <url> [<url>...]`

Fetch full page content as clean text from one or more URLs.

| Option | Description | Default |
|---|---|---|
| `-m, --max-characters` | Max characters per page | unlimited |

## Global Options

| Option | Description |
|---|---|
| `--api-key` | Exa API key (default: $EXA_API_KEY) |
| `--json` | Output JSON format |
| `--indent` | Pretty JSON format (use with --json) |


---


# How to add a skill to ai agent?

@see [skills/exa-cli-simple-skills/SKILL.md](https://github.com/wzwjustdoit/exa-cli-simple/blob/master/skills/exa-cli-simple-skills/SKILL.md)

## npx skills add
```bash
npx skills add https://github.com/wzwjustdoit/exa-cli-simple --skill exa-cli-simple-skills
```

## or manual: git clone
```bash
git clone https://github.com/wzwjustdoit/exa-cli-simple
# examples
cp -r exa-cli-simple/skills/exa-cli-simple-skills ~/.claude/skills/
cp -r exa-cli-simple/skills/exa-cli-simple-skills /path/to/your_project/.claude/skills/

# or
# ~/.codex/skills/
# ~/.config/opencode/skills/
# ~/.agents/skills/
```
