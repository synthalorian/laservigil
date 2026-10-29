from pathlib import Path

from laservigil.checks import scan_page
from laservigil.fetchers import FixtureFetcher

FIXTURES = Path(__file__).parent / "fixtures"


def _kinds(mod_id):
    return sorted((f.kind, f.ref) for f in scan_page(FixtureFetcher(FIXTURES).fetch(mod_id)))


def test_neon_skies_findings():
    assert _kinds("neon-skies") == [
        ("broken-dependency", "https://example.invalid/owl"),
        ("permission-request", "p-7"),
        ("unanswered-comment", "c-10"),  # a non-owner reply doesn't count
        ("unanswered-message", "m-1"),
    ]


def test_laser_grid_is_clean():
    assert _kinds("laser-grid") == []
