from pathlib import Path

import pytest

from laservigil.fetchers import FixtureFetcher, GitHubFetcher, ModFetcher, NexusModsFetcher

FIXTURES = Path(__file__).parent / "fixtures"


def test_fixture_fetcher_lists_and_loads():
    fetcher = FixtureFetcher(FIXTURES)
    assert fetcher.list_mods() == ["laser-grid", "neon-skies"]
    page = fetcher.fetch("neon-skies")
    assert page.source == "nexus"
    assert page.owner == "chromewave"
    assert len(page.messages) == 2


def test_fixture_fetcher_missing_mod():
    with pytest.raises(FileNotFoundError):
        FixtureFetcher(FIXTURES).fetch("does-not-exist")


@pytest.mark.parametrize("cls", [FixtureFetcher, NexusModsFetcher, GitHubFetcher])
def test_all_fetchers_satisfy_protocol(cls):
    inst = cls(FIXTURES) if cls is FixtureFetcher else cls()
    assert isinstance(inst, ModFetcher)


@pytest.mark.parametrize("cls", [NexusModsFetcher, GitHubFetcher])
def test_live_fetchers_are_stubs(cls):
    with pytest.raises(NotImplementedError):
        cls().fetch("anything")
    with pytest.raises(NotImplementedError):
        cls().list_mods()
