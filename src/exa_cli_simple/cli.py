# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Exa CLI: A CLI tool for Exa WebSearch/WebFetch

CLI Command:
  exa search    ->    web_search_exa
  exa fetch     ->    web_fetch_exa

Installation:
  pip install exa-cli-simple
  # or
  uv tool install exa-cli-simple

Usage:
  export EXA_API_KEY=your_api_key
  exa search <query> [-n NUM_RESULTS]
  exa fetch <url> [<url>...] [-m MAX_CHARACTERS]
"""

import argparse
import json
import os
import sys

from exa_py import Exa

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")


def isblank(item) -> bool:
    if item is None:
        return True
    if isinstance(item, str):
        return not item or item.isspace()
    return False


def isblanklist(lst: list) -> bool:
    if lst is None or len(lst) == 0:
        return True
    return all(isblank(item) for item in lst)


def compat_to_dict(obj):
    """Convert object to dict, compatible with Pydantic v1 (.dict()) and v2 (.model_dump())."""
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if hasattr(obj, "dict"):
        return obj.dict()
    return vars(obj)


def may_indent(args: argparse.Namespace):
    return 2 if args.pretty else None


def may_json_dumps_error(error, args: argparse.Namespace):
    return json.dumps({"error": error}, indent=may_indent(args), ensure_ascii=False) if args.json else error


def make_client(args: argparse.Namespace) -> Exa:
    api_key = args.api_key or os.environ.get("EXA_API_KEY")
    if not api_key:
        error = "Error: Exa API Key is required. Set it via `--api-key` or `EXA_API_KEY` env var."
        error = may_json_dumps_error(error, args)
        print(error, file=sys.stderr)
        sys.exit(1)
    return Exa(api_key=api_key)


def validate_args_query(args: argparse.Namespace):
    if isblank(args.query):
        error = "Error: `query` should not be blank."
        error = may_json_dumps_error(error, args)
        print(error, file=sys.stderr)
        sys.exit(1)


def validate_args_num_results(args: argparse.Namespace):
    # args.num_results
    pass


def validate_args_urls(args: argparse.Namespace):
    if isblanklist(args.urls):
        error = "Error: `urls` should not be blank."
        error = may_json_dumps_error(error, args)
        print(error, file=sys.stderr)
        sys.exit(1)


def validate_args_max_characters(args: argparse.Namespace):
    # args.max_characters
    pass


def web_search_exa(args: argparse.Namespace):
    """Search the web"""
    validate_args_query(args)
    validate_args_num_results(args)
    client = make_client(args)
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
        print(
            json.dumps(
                [compat_to_dict(r) for r in resp.results],
                indent=may_indent(args),
                ensure_ascii=False,
            )
        )
        return

    if not resp.results:
        print("Not Found: any results.")
        return
    for i, r in enumerate(resp.results):
        print(f"{i + 1}. {r.title or '(no title)'}")
        print(f"  URL: {r.url}")
        if r.score is not None:
            print(f"  Score: {r.score:.2f}")
        if r.published_date:
            print(f"  Published: {r.published_date}")
        if r.highlights:
            for h in r.highlights[:3]:
                print(f"  Highlight: {h}")
        print()


def web_fetch_exa(args: argparse.Namespace):
    """Fetch page content from URLs"""
    validate_args_urls(args)
    validate_args_max_characters(args)
    client = make_client(args)
    resp = None
    try:
        resp = client.get_contents(args.urls)
    except Exception as e:
        error = f"Error: {e}"
        error = may_json_dumps_error(error, args)
        print(error, file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(
            json.dumps(
                [compat_to_dict(r) for r in resp.results],
                indent=may_indent(args),
                ensure_ascii=False,
            )
        )
        return

    if not resp.results:
        print("Not Found: any results.")
        return
    for i, r in enumerate(resp.results):
        print(f"{i + 1}. {r.title or '(no title)'}")
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

    def add_argument_common(parser: argparse.ArgumentParser):
        parser.add_argument("--api-key", help="Exa API key (or `EXA_API_KEY` env var)")
        parser.add_argument("--json", "-j", action="store_true", help="Output JSON format")
        parser.add_argument("--pretty", "-p", action="store_true", help="Pretty JSON format (use with --json)")
        parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS, help="show this help message and exit")

    root_parser = argparse.ArgumentParser(
        prog="exa",
        description=str(
            "Exa CLI: A CLI tool for Exa WebSearch/WebFetch"
            + "\n\n"
            + "usage: exa {search,fetch} ..."
        ),
        usage=argparse.SUPPRESS,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    root_parser.set_defaults(func=lambda args: root_parser.print_help())

    sub = root_parser.add_subparsers()

    search_parser = sub.add_parser(
        "search",
        prog="exa search",
        description=str(
            "Exa WebSearch"
            + "\n\n"
            + "usage: exa search <query> [-n NUM_RESULTS] [--api-key API_KEY] [--json] [--pretty]"
        ),
        usage=argparse.SUPPRESS,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help="Search the web",
        add_help=False,
    )
    search_parser.add_argument("query", help="The query text (describe the ideal page, not keywords)")
    search_parser.add_argument("-n", "--num-results", type=int, default=10, help="Number of results (default: 10)")
    add_argument_common(search_parser)
    search_parser.set_defaults(func=web_search_exa)

    fetch_parser = sub.add_parser(
        "fetch",
        prog="exa fetch",
        description=str(
            "Exa WebFetch"
            + "\n\n"
            + "usage: exa fetch <url> [<url>...] [-m MAX_CHARACTERS] [--api-key API_KEY] [--json] [--pretty]"
        ),
        usage=argparse.SUPPRESS,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help="Fetch page content from URLs",
        add_help=False,
    )
    fetch_parser.add_argument("urls", nargs="+", help="One or more URLs to fetch")
    fetch_parser.add_argument("-m", "--max-characters", type=int, default=None, help="Max characters per page (default: not restricted)")
    add_argument_common(fetch_parser)
    fetch_parser.set_defaults(func=web_fetch_exa)

    args = root_parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
