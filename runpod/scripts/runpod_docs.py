#!/usr/bin/env python3
"""Fetch and search official Runpod docs.

Examples:
  python runpod_docs.py search serverless handler
  python runpod_docs.py page serverless/workers/handler-functions
  python runpod_docs.py openapi --output /tmp/runpod-openapi.json
  python runpod_docs.py openapi --version v1 --output /tmp/runpod-v1-openapi.json
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


DOCS_ROOT = "https://docs.runpod.io"
LLMS_URL = f"{DOCS_ROOT}/llms.txt"
OPENAPI_URLS = {
    "v1": "https://rest.runpod.io/v1/openapi.json",
    "v2": "https://api.runpod.io/v2/openapi.json",
}


def fetch(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "codex-runpod-skill/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"HTTP {exc.code} fetching {url}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Error fetching {url}: {exc.reason}") from exc


def docs_url(value: str) -> str:
    if value.startswith("http://") or value.startswith("https://"):
        url = value
    else:
        url = f"{DOCS_ROOT}/{value.lstrip('/')}"

    parsed = urllib.parse.urlparse(url)
    if parsed.netloc == "docs.runpod.io" and not Path(parsed.path).suffix:
        parsed = parsed._replace(path=f"{parsed.path}.md")
        url = urllib.parse.urlunparse(parsed)
    return url


def write_or_print(text: str, output: str | None) -> None:
    if output:
        Path(output).write_text(text, encoding="utf-8")
        print(output)
    else:
        print(text)


def command_index(args: argparse.Namespace) -> None:
    write_or_print(fetch(LLMS_URL), args.output)


def command_search(args: argparse.Namespace) -> None:
    haystack = fetch(LLMS_URL)
    terms = [term.casefold() for term in args.terms]
    matches = []
    for raw_line in haystack.splitlines():
        line = raw_line.strip()
        folded = line.casefold()
        if all(term in folded for term in terms):
            matches.append(line)

    if args.json:
        write_or_print(json.dumps(matches, indent=2), args.output)
    else:
        write_or_print("\n".join(matches), args.output)


def command_page(args: argparse.Namespace) -> None:
    write_or_print(fetch(docs_url(args.page)), args.output)


def command_openapi(args: argparse.Namespace) -> None:
    write_or_print(fetch(OPENAPI_URLS[args.version]), args.output)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fetch and search official Runpod docs")
    subcommands = parser.add_subparsers(dest="command", required=True)

    index = subcommands.add_parser("index", help="Fetch https://docs.runpod.io/llms.txt")
    index.add_argument("--output", help="Write output to a file")
    index.set_defaults(func=command_index)

    search = subcommands.add_parser("search", help="Search the docs index for terms")
    search.add_argument("terms", nargs="+", help="Terms that must all appear on a matching line")
    search.add_argument("--json", action="store_true", help="Emit JSON array")
    search.add_argument("--output", help="Write output to a file")
    search.set_defaults(func=command_search)

    page = subcommands.add_parser("page", help="Fetch a docs page by path or URL")
    page.add_argument("page", help="Example: serverless/workers/handler-functions")
    page.add_argument("--output", help="Write output to a file")
    page.set_defaults(func=command_page)

    openapi = subcommands.add_parser("openapi", help="Fetch the REST OpenAPI JSON")
    openapi.add_argument("--version", choices=sorted(OPENAPI_URLS), default="v2", help="API version (default: v2)")
    openapi.add_argument("--output", help="Write output to a file")
    openapi.set_defaults(func=command_openapi)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
