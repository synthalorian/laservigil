import io

from laservigil import color
from laservigil.color import Palette, color_enabled


class FakeTTY(io.StringIO):
    def isatty(self) -> bool:
        return True


def test_color_on_for_tty_without_no_color():
    assert color_enabled(FakeTTY(), env={}) is True


def test_no_color_env_disables_color():
    assert color_enabled(FakeTTY(), env={"NO_COLOR": "1"}) is False


def test_empty_no_color_does_not_disable():
    # Per no-color.org, only a non-empty value counts.
    assert color_enabled(FakeTTY(), env={"NO_COLOR": ""}) is True


def test_non_tty_disables_color():
    assert color_enabled(io.StringIO(), env={}) is False


def test_palette_off_passes_text_through():
    pal = Palette(enabled=False)
    for styled in (pal.cyan("x"), pal.magenta("x", bold=True), pal.glow("x"), pal.accent("x")):
        assert styled == "x"


def test_palette_on_uses_cyan_magenta_on_black():
    pal = Palette(enabled=True)
    assert pal.cyan("x") == f"{color.CYAN}x{color.RESET}"
    assert pal.magenta("x") == f"{color.MAGENTA}x{color.RESET}"
    assert ";40m" in color.CYAN and ";40m" in color.MAGENTA


def test_for_stream_respects_env(monkeypatch):
    monkeypatch.setenv("NO_COLOR", "yes")
    assert Palette.for_stream(FakeTTY()).enabled is False
    monkeypatch.delenv("NO_COLOR")
    assert Palette.for_stream(FakeTTY()).enabled is True
