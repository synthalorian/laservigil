"""Data model for a fetched mod page and the findings derived from it."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Thread:
    """A message or comment, plus the handles of everyone who replied."""

    id: str
    author: str
    body: str
    repliers: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Thread":
        replies = data.get("replies", [])
        return cls(
            id=str(data["id"]),
            author=str(data["author"]),
            body=str(data.get("body", "")),
            repliers=tuple(str(r["author"]) for r in replies),
        )


@dataclass(frozen=True)
class PermissionRequest:
    id: str
    requester: str
    asset: str
    status: str = "pending"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PermissionRequest":
        return cls(
            id=str(data["id"]),
            requester=str(data["requester"]),
            asset=str(data.get("asset", "")),
            status=str(data.get("status", "pending")),
        )


@dataclass(frozen=True)
class Dependency:
    name: str
    status: str = "ok"  # ok | missing | removed | outdated
    url: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Dependency":
        return cls(
            name=str(data["name"]),
            status=str(data.get("status", "ok")),
            url=str(data.get("url", "")),
        )


@dataclass(frozen=True)
class ModPage:
    source: str  # "nexus" | "github"
    mod_id: str
    title: str
    owner: str
    messages: tuple[Thread, ...] = ()
    comments: tuple[Thread, ...] = ()
    permission_requests: tuple[PermissionRequest, ...] = ()
    dependencies: tuple[Dependency, ...] = ()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ModPage":
        try:
            return cls(
                source=str(data["source"]),
                mod_id=str(data["mod_id"]),
                title=str(data.get("title", data["mod_id"])),
                owner=str(data["owner"]),
                messages=tuple(Thread.from_dict(m) for m in data.get("messages", [])),
                comments=tuple(Thread.from_dict(c) for c in data.get("comments", [])),
                permission_requests=tuple(
                    PermissionRequest.from_dict(p)
                    for p in data.get("permission_requests", [])
                ),
                dependencies=tuple(
                    Dependency.from_dict(d) for d in data.get("dependencies", [])
                ),
            )
        except KeyError as exc:
            raise ValueError(f"mod page is missing required field {exc}") from exc


@dataclass(frozen=True)
class Finding:
    kind: str  # unanswered-message | unanswered-comment | permission-request | broken-dependency
    mod_id: str
    source: str
    summary: str
    ref: str = ""
    extra: dict[str, str] = field(default_factory=dict, compare=False)
