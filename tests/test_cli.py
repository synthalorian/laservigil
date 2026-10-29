import io
import json
from pathlib import Path

from laservigil import NAME, VERSION
from laservigil.cli import main

FIXTURES = str(Path(__file__).parent / "fixtures")


class FakeTTY(io.StringIO):
    def isatty(self) -> bool:
        return True


def run(argv, out=None):
    out = io.StringIO() if out is None else out
    err = io.StringIO()
    code = main(argv, out=out, err=err)
    return code, out.getvalue(), err.getvalue()


def test_scan_plain_output_has_no_ansi_when_not_tty(monkeypatch):
    monkeypatch.delenv("NO_COLOR", raising=False)
    code, out, _ = run(["scan", "--fixtures", FIXTURES])
    assert code == 0
    assert "\033[" not in out
    assert "4 finding(s) across 2 mod page(s)" in out
    assert "[PERM]" in out


def test_scan_colored_on_tty(monkeypatch):
    monkeypatch.delenv("NO_COLOR", raising=False)
    _, out, _ = run(["scan", "--fixtures", FIXTURES], out=FakeTTY())
    assert "\033[35;40m" in out and "\033[36;40m" in out


def test_scan_no_color_env_on_tty(monkeypatch):
    monkeypatch.setenv("NO_COLOR", "1")
    _, out, _ = run(["scan", "--fixtures", FIXTURES], out=FakeTTY())
    assert "\033[" not in out


def test_scan_clean_mod_and_strict():
    code, out, _ = run(["scan", "--fixtures", FIXTURES, "--strict", "laser-grid"])
    assert code == 0
    assert "all quiet on the grid" in out
    code, _, _ = run(["scan", "--fixtures", FIXTURES, "--strict", "neon-skies"])
    assert code == 1


def test_scan_json():
    code, out, _ = run(["scan", "--fixtures", FIXTURES, "--json", "neon-skies"])
    assert code == 0
    assert {f["kind"] for f in json.loads(out)} == {
        "unanswered-message", "unanswered-comment", "permission-request", "broken-dependency",
    }


def test_live_source_reports_not_implemented():
    code, _, err = run(["scan", "--source", "nexus"])
    assert code == 2
    assert "not implemented" in err


def test_missing_fixture_is_an_error():
    code, _, err = run(["scan", "--fixtures", FIXTURES, "nope"])
    assert code == 2 and "nope" in err


def test_version(capsys):
    try:
        main(["--version"])
    except SystemExit as exc:
        assert exc.code == 0
    assert capsys.readouterr().out.strip() == f"{NAME} {VERSION}"
