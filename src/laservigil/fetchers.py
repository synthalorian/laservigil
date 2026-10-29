"""Fetcher interface plus fixture-backed and (stubbed) live implementations."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Protocol, runtime_checkable

from .models import ModPage


@runtime_checkable
class ModFetcher(Protocol):
    """Anything that can turn a mod id into a ModPage."""

    source: str

    def fetch(self, mod_id: str) -> ModPage: ...

    def list_mods(self) -> Iterable[str]: ...


class FixtureFetcher:
    """Reads ModPage data from ``<directory>/<mod_id>.json``. Never touches the network.

    Raises ``FileNotFoundError`` if ``directory`` does not exist and
    ``NotADirectoryError`` if it exists but is not a directory.
    """

    def __init__(self, directory: str | Path, source: str = "fixture") -> None:
        self.directory = Path(directory)
        if not self.directory.exists():
            raise FileNotFoundError(f"fixture directory not found: {self.directory}")
        if not self.directory.is_dir():
            raise NotADirectoryError(f"fixture path is not a directory: {self.directory}")
        self.source = source

    def list_mods(self) -> list[str]:
        return sorted(p.stem for p in self.directory.glob("*.json"))

    def fetch(self, mod_id: str) -> ModPage:
        path = self.directory / f"{mod_id}.json"
        if not path.is_file():
            raise FileNotFoundError(f"no fixture for mod {mod_id!r} at {path}")
        with path.open(encoding="utf-8") as fh:
            data = json.load(fh)
        return ModPage.from_dict(data)


class NexusModsFetcher:
    """Live Nexus Mods fetcher. Not implemented yet."""

    source = "nexus"

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key

    def list_mods(self) -> Iterable[str]:
        raise NotImplementedError("live Nexus Mods fetching is not implemented yet")

    def fetch(self, mod_id: str) -> ModPage:
        raise NotImplementedError("live Nexus Mods fetching is not implemented yet")


class GitHubFetcher:
    """Live GitHub fetcher (issues, discussions, release deps). Not implemented yet."""

    source = "github"

    def __init__(self, token: str | None = None) -> None:
        self.token = token

    def list_mods(self) -> Iterable[str]:
        raise NotImplementedError("live GitHub fetching is not implemented yet")

    def fetch(self, mod_id: str) -> ModPage:
        raise NotImplementedError("live GitHub fetching is not implemented yet")
