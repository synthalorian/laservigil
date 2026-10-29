"""Command-line entry point."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from typing import Sequence, TextIO

from ._meta import NAME, TAGLINE, VERSION
from .checks import scan_page
from .color import Palette
from .fetchers import FixtureFetcher, GitHubFetcher, ModFetcher, NexusModsFetcher
from .models import Finding

KIND_LABELS = {
    "unanswered-message": "MSG",
    "unanswered-comment": "CMT",
    "permission-request": "PERM",
    "broken-dependency": "DEP",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=NAME, description=f"{NAME} — {TAGLINE}")
    parser.add_argument("--version", action="version", version=f"{NAME} {VERSION}")
    sub = parser.add_subparsers(dest="command")

    scan = sub.add_parser("scan", help="scan mod pages for things that need you")
    group = scan.add_mutually_exclusive_group(required=True)
    group.add_argument("--fixtures", metavar="DIR", help="read mod pages from JSON fixtures in DIR")
    group.add_argument("--source", choices=["nexus", "github"], help="live source (not implemented yet)")
    scan.add_argument("mods", nargs="*", metavar="MOD_ID", help="mod ids to scan (default: all fixtures)")
    scan.add_argument("--json", action="store_true", help="emit findings as JSON")
    scan.add_argument("--strict", action="store_true", help="exit 1 if anything is found")
    return parser


def _make_fetcher(args: argparse.Namespace) -> ModFetcher:
    if args.fixtures:
        return FixtureFetcher(args.fixtures)
    if args.source == "nexus":
        return NexusModsFetcher()
    return GitHubFetcher()


def _render(findings: list[Finding], scanned: int, pal: Palette, out: TextIO) -> None:
    print(pal.glow(f"// {NAME.upper()} :: {TAGLINE}"), file=out)
    for f in findings:
        label = KIND_LABELS.get(f.kind, f.kind)
        ref = f" {pal.accent(f.ref)}" if f.ref else ""
        print(
            f"{pal.magenta(f'[{label:>4}]', bold=True)} "
            f"{pal.cyan(f'{f.source}/{f.mod_id}')}{ref} {f.summary}",
            file=out,
        )
    tally = f"{len(findings)} finding(s) across {scanned} mod page(s)"
    print(pal.magenta(tally) if findings else pal.cyan(f"all quiet on the grid — {tally}"), file=out)


def cmd_scan(args: argparse.Namespace, out: TextIO, err: TextIO) -> int:
    fetcher = _make_fetcher(args)
    try:
        mod_ids = list(args.mods) or list(fetcher.list_mods())
        findings: list[Finding] = []
        for mod_id in mod_ids:
            findings.extend(scan_page(fetcher.fetch(mod_id)))
    except NotImplementedError as exc:
        print(f"{NAME}: {exc}", file=err)
        return 2
    except (OSError, ValueError) as exc:
        print(f"{NAME}: {exc}", file=err)
        return 2

    if args.json:
        json.dump([asdict(f) for f in findings], out, indent=2)
        out.write("\n")
    else:
        _render(findings, len(mod_ids), Palette.for_stream(out), out)
    return 1 if (args.strict and findings) else 0


def main(argv: Sequence[str] | None = None, out: TextIO | None = None, err: TextIO | None = None) -> int:
    out = sys.stdout if out is None else out
    err = sys.stderr if err is None else err
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "scan":
        return cmd_scan(args, out, err)
    parser.print_help(out)
    return 0
