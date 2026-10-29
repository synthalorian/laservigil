<p align="center"><img src=".github/assets/laservigil-banner.png" alt="laservigil banner" width="100%"></p>

# Laservigil

> **The neon-lit sentinel for your mod pages.** 🌆

It's 2 AM. The city hums in magenta. Somewhere on Nexus Mods, a user has been
waiting three days for an answer about a crash. On GitHub, someone asked
permission to reuse your textures. And that library your mod depends on? It
quietly vanished off the grid.

**Laservigil** scans your Nexus Mods and GitHub mod pages and lights up everything
that needs you:

- 💬 **Unanswered messages & comments** — threads started by someone else that you, the owner, never replied to (replies from other users don't count).
- 🔑 **Pending permission requests** — anyone waiting on a yes/no to use your assets.
- ⛓️ **Broken dependencies** — requirements marked `missing`, `removed`, or `outdated`.

Pure Python standard library. No dependencies. No telemetry. Just you, the
grid, and a terminal glowing cyan on black.

> ⚠️ **Status: early prototype.** Live fetchers for Nexus Mods and GitHub are
> stubs that raise `NotImplementedError`. Today, Laservigil runs against JSON
> fixtures, so you can try the pipeline and build integrations against a stable
> data shape.

## Usage

Requires Python 3.10+.

```sh
pip install .            # or skip installing and use: PYTHONPATH=src python3 -m laservigil
laservigil scan --fixtures tests/fixtures
```

```
// LASERVIGIL :: neon-lit sentinel for your mod pages
[ MSG] nexus/neon-skies m-1 @gridrunner: Crash on load with v2.1?
[ CMT] nexus/neon-skies c-10 @retrofox: Does this work with the night patch?
[PERM] nexus/neon-skies p-7 @synthcrafter wants to use sky textures
[ DEP] nexus/neon-skies https://example.invalid/owl Old Weather Lib is removed
4 finding(s) across 2 mod page(s)
```

| Command / flag | What it does |
| --- | --- |
| `laservigil scan --fixtures DIR [MOD_ID ...]` | Scan the `<MOD_ID>.json` fixtures in `DIR` (all of them if you list no ids) |
| `laservigil scan --source nexus\|github` | Live mode. Reserved; not implemented yet, so it exits with code 2 |
| `--json` | Print findings as a JSON array, for scripts and dashboards |
| `--strict` | Exit `1` if anything turns up (handy in cron jobs or CI) |
| `--version` | Print the version |

**Exit codes:** `0` scan finished · `1` findings were reported with `--strict` · `2` error (missing fixture, bad JSON, live source not implemented).

### Color

Output uses a cyan and magenta palette on a black background. Laservigil turns
color off when:

- the [`NO_COLOR`](https://no-color.org) environment variable is set to a non-empty value, or
- stdout is not a TTY (pipes, files, CI logs).

### Fixture format

```json
{
  "source": "nexus",
  "mod_id": "neon-skies",
  "title": "Neon Skies Weather Overhaul",
  "owner": "chromewave",
  "messages":  [{"id": "m-1", "author": "gridrunner", "body": "...", "replies": [{"author": "chromewave"}]}],
  "comments":  [{"id": "c-10", "author": "retrofox", "body": "...", "replies": []}],
  "permission_requests": [{"id": "p-7", "requester": "synthcrafter", "asset": "sky textures", "status": "pending"}],
  "dependencies": [{"name": "Old Weather Lib", "status": "removed", "url": "https://example.invalid/owl"}]
}
```

`source`, `mod_id` and `owner` are required. Everything else is optional.

## Architecture

```
src/laservigil/
├── _meta.py     # NAME / VERSION / TAGLINE: the single source of truth
├── color.py     # the only place ANSI codes live (NO_COLOR + TTY aware)
├── models.py    # ModPage, Thread, PermissionRequest, Dependency, Finding
├── fetchers.py  # ModFetcher Protocol, FixtureFetcher, live stubs
├── checks.py    # pure scan_page(ModPage) -> list[Finding]
└── cli.py       # argparse front end
```

To add a live source, implement the `ModFetcher` protocol (`source`,
`fetch(mod_id) -> ModPage`, `list_mods()`). The checks don't care where the
data came from.

## Development

```sh
python3 -m pip install pytest
python3 -m pytest -q
```

No install step is needed. The root `conftest.py` and the pytest `pythonpath`
setting put `src/` on the import path. The tests use only local JSON fixtures
and never make network calls. CI runs the suite on Python 3.10 to 3.13
(`.github/workflows/ci.yml`).

Renaming the project? See [RENAME.md](RENAME.md).

## License

MIT. See [LICENSE](LICENSE).
