"""Pure functions that scan a ModPage and emit Findings."""

from __future__ import annotations

from .models import Finding, ModPage, Thread

BROKEN_DEP_STATUSES = frozenset({"missing", "removed", "outdated"})


def _unanswered(threads: tuple[Thread, ...], owner: str) -> list[Thread]:
    """Threads started by someone other than the owner with no owner reply."""
    return [t for t in threads if t.author != owner and owner not in t.repliers]


def scan_page(page: ModPage) -> list[Finding]:
    findings: list[Finding] = []
    for kind, threads in (
        ("unanswered-message", page.messages),
        ("unanswered-comment", page.comments),
    ):
        for t in _unanswered(threads, page.owner):
            findings.append(
                Finding(kind, page.mod_id, page.source, f"@{t.author}: {t.body}", ref=t.id)
            )
    for req in page.permission_requests:
        if req.status == "pending":
            findings.append(
                Finding(
                    "permission-request",
                    page.mod_id,
                    page.source,
                    f"@{req.requester} wants to use {req.asset or 'assets'}",
                    ref=req.id,
                )
            )
    for dep in page.dependencies:
        if dep.status in BROKEN_DEP_STATUSES:
            findings.append(
                Finding(
                    "broken-dependency",
                    page.mod_id,
                    page.source,
                    f"{dep.name} is {dep.status}",
                    ref=dep.url,
                )
            )
    return findings
