# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Exa CLI - A CLI tool for Exa WebSearch/WebFetch

CLI Command:
  exa search    ->    web_search_exa
  exa fetch     ->    web_fetch_exa

Installation:
  pip install exa-cli-simple
  # or
  uv tool install exa-cli-simple

Usage:
  export EXA_API_KEY=your_key
  exa search <query> [--num-results N]
  exa fetch <url> [<url>...] [--max-characters N]
"""

import argparse
import json
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
from exa_py import Exa


def may_indent(args: argparse.Namespace):
    return 2 if args.indent else None


def may_json_dumps_error(error, args: argparse.Namespace):
    return json.dumps({"error": error}, indent=may_indent(args), ensure_ascii=False) if args.json else error


def compat_to_dict(obj):
    """Convert object to dict, compatible with Pydantic v1 (.dict()) and v2 (.model_dump())."""
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if hasattr(obj, "dict"):
        return obj.dict()
    return vars(obj)


def get_client(args: argparse.Namespace) -> Exa:
    api_key = args.api_key or os.environ.get("EXA_API_KEY")
    if not api_key:
        error = "Error: EXA_API_KEY is required. Set it via --api-key or EXA_API_KEY env var."
        error = may_json_dumps_error(error, args)
        print(error, file=sys.stderr)
        sys.exit(1)
    return Exa(api_key=api_key)


def web_search_exa(args: argparse.Namespace) -> None:
    """search the web and get clean content."""
    client = get_client(args)
    resp = None
    try:
        resp = client.search(
            args.query,
            num_results=args.num_results,
            contents={"highlights": True},
        )
    except Exception as e:
        error = f"Error: {e}"
        error = may_json_dumps_error(error, args)
        print(error, file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps([compat_to_dict(r) for r in resp.results], indent=may_indent(args), ensure_ascii=False))
        return

    if not resp.results:
        print("No results found.")
        return

    for i, r in enumerate(resp.results, 1):
        print(f"{i}. {r.title or '(no title)'}")
        print(f"  URL: {r.url}")
        if r.score is not None:
            print(f"  Score: {r.score:.2f}")
        if r.published_date:
            print(f"  Published: {r.published_date}")
        if r.highlights:
            for h in r.highlights[:3]:
                print(f"  -> {h}")
        print()


def web_fetch_exa(args: argparse.Namespace) -> None:
    """fetch page content as clean text from one or more URLs."""
    client = get_client(args)
    resp = None
    try:
        resp = client.get_contents(args.urls)
    except Exception as e:
        error = f"Error: {e}"
        error = may_json_dumps_error(error, args)
        print(error, file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps([compat_to_dict(r) for r in resp.results], indent=may_indent(args), ensure_ascii=False))
        return

    if not resp.results:
        print("No results found.")
        return

    for r in resp.results:
        header = r.title or r.url
        print(f"--- {header} ---")
        print(f"URL: {r.url}")
        if r.text:
            text = r.text
            if args.max_characters and args.max_characters > 0 and len(text) > args.max_characters:
                text = text[: args.max_characters] + "\n... [truncated]"
            print(text)
        else:
            print("(no text content)")
        print()


def main():
    parser = argparse.ArgumentParser(
        prog="exa",
        description="Exa CLI - A CLI tool for Exa WebSearch/WebFetch",
    )

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument("--api-key", help="Exa API key (default: $EXA_API_KEY)")
    parent_parser.add_argument("--json", action="store_true", help="Output JSON format")
    parent_parser.add_argument("--indent", action="store_true", help="Pretty JSON format (use with --json)")

    sub = parser.add_subparsers(dest="command", required=True)

    p_search = sub.add_parser("search", parents=[parent_parser, ], help="Search the web (web_search_exa)")
    p_search.add_argument("query", help="Search query (describe the ideal page, not keywords)")
    p_search.add_argument("-n", "--num-results", type=int, default=10, help="Number of results (default: 10)")
    p_search.set_defaults(func=web_search_exa)

    p_fetch = sub.add_parser("fetch", parents=[parent_parser, ], help="Fetch page content from URLs (web_fetch_exa)")
    p_fetch.add_argument("urls", nargs="+", help="One or more URLs to fetch")
    p_fetch.add_argument("-m", "--max-characters", type=int, default=None, help="Max characters per page (default: unlimited)")
    p_fetch.set_defaults(func=web_fetch_exa)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
