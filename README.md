# About: exa-cli-simple

Exa CLI: A CLI tool for Exa WebSearch/WebFetch

## Installation

```bash
pip install exa-cli-simple
# or
uv tool install exa-cli-simple
```

## Usage

```bash
export EXA_API_KEY=your_api_key
exa search "how to use exa python sdk?"
exa search "how to use exa python sdk?" -n 3 --json
exa fetch "https://exa.ai/docs/sdks/python-sdk"
exa fetch "https://exa.ai/docs/sdks/python-sdk" -m 1000 --json
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
| `-m, --max-characters` | Max characters per page | not restricted |

## Global Options

| Option | Description |
|---|---|
| `--api-key` | Exa API key (or `EXA_API_KEY` env var) |
| `--json` | Output JSON format |
| `--pretty` | Pretty JSON format (use with --json) |


---


# How to add this skill to ai agent?

@see [skills/exa-cli-simple-skills/SKILL.md](https://github.com/wzwjustdoit/exa-cli-simple/blob/master/skills/exa-cli-simple-skills/SKILL.md)

## npx skills add
```bash
npx skills add https://github.com/wzwjustdoit/exa-cli-simple --skill exa-cli-simple-skills
```

## or manual: git clone
```bash
git clone https://github.com/wzwjustdoit/exa-cli-simple
# examples:
cp -r exa-cli-simple/skills/exa-cli-simple-skills ~/.claude/skills/
cp -r exa-cli-simple/skills/exa-cli-simple-skills /path/to/your_project/.claude/skills/

# more:
# ~/.agents/skills/
# ~/.codex/skills/
# ~/.config/opencode/skills/
# ~/.codebuddy/skills/
# ~/.continue/skills/
# ~/.cursor/skills/
# ~/.hermes/skills/
# ~/.pi/agent/skills//
# ~/.qoder/skills/
# ~/.qwen/skills/
# ~/.trae/skills/
# ~/.windsurf/skills/
```
