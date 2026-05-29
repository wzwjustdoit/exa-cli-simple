---
name: exa-cli-simple
description: >
  CLI 工具，封装 Exa 搜索引擎的 WebSearch 和 WebFetch API。
  当用户需要搜索互联网、查找最新信息、获取网页内容时触发。
  适合回答需要实时/最新信息的问题，或者批量获取多个 URL 的正文内容。
---

# exa-cli-simple Skill

本 skill 基于 `exa-cli-simple` 项目，提供通过终端使用 Exa 搜索引擎的能力。

## 何时使用

- 用户需要**搜索互联网**获取最新信息（新闻、文档、人物、公司）
- 用户需要**获取某个 URL 的正文内容**（支持批量）
- 用户需要**查询某个主题的当前/真实信息**
- 用户需要**验证或补充知识库中没有的信息**
- 适合替代内置 web_search/web_fetch 能力，提供更干净更结构化的结果

## 前置条件

- 已安装 `exa-cli-simple`:
  `pip install exa-cli-simple` 或 `uv tool install exa-cli-simple`
- 已设置环境变量 `EXA_API_KEY` (或每次传参 `--api-key` )

## 基础用法

### 1. `exa search <query>` — 搜索

```bash
exa search "<query>" [选项]
```

**查询技巧**: 描述你想要的页面，而非关键词。
- ✅ `"blog post comparing React and Vue performance 2025"`
- ❌ `"React vs Vue"`

**选项**:
| 选项 | 作用 | 默认 |
|---|---|---|
| `-n <N>` | 返回结果数量 | 10 |
| `--json` | JSON 格式输出 | 无 |
| `--pretty` | 格式化 JSON（需配合 --json） | 无 |

**示例**:
```bash
# 普通搜索，默认输出文本格式
exa search "how to use exa python sdk?"

# JSON 输出，方便后续处理
exa search "latest AI news 2026" -n 5 --json

# 格式化 JSON
exa search "best practices for CLI tools" --json --pretty

# 限制结果数量
exa search "category:company OpenAI funding" -n 3
```

### 2. `exa fetch <url> [<url>...]` — 获取页面内容

```bash
exa fetch <url> [<url>...] [选项]
```

**选项**:
| 选项 | 作用 | 默认 |
|---|---|---|
| `-m <N>` | 每页最大字符数 | 不限 |
| `--json` | JSON 格式输出 | 无 |
| `--pretty` | 格式化 JSON（需配合 --json） | 无 |

**示例**:
```bash
# 获取单个 URL
exa fetch "https://exa.ai/docs"

# 获取多个 URL
exa fetch "https://exa.ai/docs" "https://exa.ai/blog"

# 限制字符数
exa fetch "https://example.com/long-article" -m 2000

# JSON 输出
exa fetch "https://exa.ai" --json
```

## 在 Agent 中使用（结构化数据）

当需要在代码中处理结果时，始终使用 `--json` 标志以获得结构化输出:

```bash
# 搜索并获取 JSON 然后用 jq 或 Python 解析
exa search "python async patterns" -n 5 --json | jq
```

## 最佳实践

1. **搜索优先，抓取其次**: 先用 `exa search` 找到相关页面，如果摘要不够用，再用 `exa fetch` 获取全文
2. **语义化查询**: Exa 搜索引擎基于语义理解，查询应该像在和搜索引擎对话一样描述你想要的页面
3. **合理设置结果数**: 默认 10 条通常足够，需要更多或更少时用 `-n` 调整
4. **善用 JSON 模式**: 当结果需要被进一步程序处理时，使用 `--json`
5. **批量 URL 获取**: `exa fetch` 支持一次传入多个 URL，减少多次调用的开销
6. **截断长内容**: 用 `-m` 参数控制每页的最大字符数，避免输出过长

## 注意事项

- API Key 可通过 `--api-key` 参数传入，或通过 `EXA_API_KEY` 环境变量设置
- 搜索查询**不是关键词匹配**，而是语义匹配 — 描述你想要的内容类型
- 使用 `category:people` 或 `category:company` 可以限定搜索 LinkedIn 个人资料或公司页面
- `exa search` 的结果中包含 highlights（摘要高亮），如果不够详细，再对具体 URL 使用 `exa fetch`
