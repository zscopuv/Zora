import argparse
from types import SimpleNamespace

import pytest

from zora.cli import Zora

def make_zora(
    length=16,
    count=1,
    charset="abc123",
    unsafe=False,
    seed=None,
    quiet=False,
):
    zora = Zora()
    zora.parser = argparse.ArgumentParser()

    zora.args = SimpleNamespace(
        length=length,
        count=count,
        charset=charset,
        unsafe=unsafe,
        seed=seed,
        quiet=quiet,
    )

    zora.charset = charset

    zora.start_timer()

    return zora

def test_benchmark_runs(capsys):
    zora = make_zora()

    with pytest.raises(SystemExit) as exc_info:
        zora.calculate_benchmark()

    assert exc_info.value.code == 0


def test_benchmark_displays_title(capsys):
    zora = make_zora()

    with pytest.raises(SystemExit):
        zora.calculate_benchmark()

    output = capsys.readouterr().out

    assert "Zora Benchmark" in output


def test_benchmark_displays_csprng(capsys):
    zora = make_zora(unsafe=False)

    with pytest.raises(SystemExit):
        zora.calculate_benchmark()

    output = capsys.readouterr().out

    assert "CSPRNG" in output


def test_benchmark_displays_prng(capsys):
    zora = make_zora(unsafe=True)

    with pytest.raises(SystemExit):
        zora.calculate_benchmark()

    output = capsys.readouterr().out

    assert "PRNG" in output


def test_benchmark_displays_length(capsys):
    zora = make_zora(length=32)

    with pytest.raises(SystemExit):
        zora.calculate_benchmark()

    output = capsys.readouterr().out

    assert "Length: 32" in output


def test_benchmark_displays_count(capsys):
    zora = make_zora(count=10)

    with pytest.raises(SystemExit):
        zora.calculate_benchmark()

    output = capsys.readouterr().out

    assert "Count: 10" in output


def test_benchmark_displays_charset_size(capsys):
    zora = make_zora(charset="abcdef")

    with pytest.raises(SystemExit):
        zora.calculate_benchmark()

    output = capsys.readouterr().out

    assert "Charset: 6" in output


def test_benchmark_displays_character_count(capsys):
    zora = make_zora(length=16, count=10)

    with pytest.raises(SystemExit):
        zora.calculate_benchmark()

    output = capsys.readouterr().out

    assert "Characters: 160" in output


def test_benchmark_displays_rates(capsys):
    zora = make_zora()

    with pytest.raises(SystemExit):
        zora.calculate_benchmark()

    output = capsys.readouterr().out

    assert "Keys/sec:" in output
    assert "Characters/sec:" in output


def test_seeded_unsafe_benchmark_is_reproducible():
    zora1 = make_zora(
        length=16,
        count=5,
        unsafe=True,
        seed="test-seed",
    )

    zora2 = make_zora(
        length=16,
        count=5,
        unsafe=True,
        seed="test-seed",
    )

    with pytest.raises(SystemExit):
        zora1.calculate_benchmark()

    with pytest.raises(SystemExit):
        zora2.calculate_benchmark()


def test_benchmark_sets_elapsed():
    zora = make_zora()

    with pytest.raises(SystemExit):
        zora.calculate_benchmark()

    assert hasattr(zora, "elapsed")
    assert zora.elapsed >= 0