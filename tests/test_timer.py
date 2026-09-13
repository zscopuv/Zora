import argparse
from types import SimpleNamespace

from zora.cli import Zora


def make_zora(quiet=False):
    zora = Zora()
    zora.parser = argparse.ArgumentParser()

    zora.args = SimpleNamespace(
        quiet=quiet,
    )

    return zora


def test_start_timer_creates_start_time():
    zora = make_zora()

    zora.start_timer()

    assert hasattr(zora, "time_start")
    assert isinstance(zora.time_start, float)


def test_show_timer_creates_elapsed(capsys):
    zora = make_zora()

    zora.start_timer()
    zora.show_timer()

    assert hasattr(zora, "elapsed")
    assert zora.elapsed >= 0

    output = capsys.readouterr().out
    assert "Timer:" in output


def test_show_timer_displays_milliseconds(capsys):
    zora = make_zora()

    zora.start_timer()
    zora.show_timer()

    output = capsys.readouterr().out

    assert "ms elapsed" in output


def test_show_timer_displays_seconds(monkeypatch, capsys):
    zora = make_zora()

    zora.start_timer()

    monkeypatch.setattr(
        "zora.cli.time.perf_counter",
        lambda: zora.time_start + 2.5,
    )

    zora.show_timer()

    output = capsys.readouterr().out

    assert "2s elapsed" in output


def test_show_timer_displays_minutes(monkeypatch, capsys):
    zora = make_zora()

    zora.time_start = 1000.0

    monkeypatch.setattr(
        "zora.cli.time.perf_counter",
        lambda: 1065.0,
    )

    zora.show_timer()

    output = capsys.readouterr().out

    assert "1m 5s elapsed" in output

def test_show_timer_displays_hours(monkeypatch, capsys):
    zora = make_zora()

    zora.time_start = 1000.0

    monkeypatch.setattr(
        "zora.cli.time.perf_counter",
        lambda: 4665.0,
    )

    zora.show_timer()

    output = capsys.readouterr().out

    assert "1h 1m 5s elapsed" in output


def test_show_timer_without_start_does_not_crash(capsys):
    zora = make_zora()

    zora.show_timer()

    output = capsys.readouterr().out

    assert "Timer has not been started properly." in output