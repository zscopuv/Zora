import argparse
from types import SimpleNamespace

import pytest

from zora.cli import Zora


def make_zora(
    length=16,
    seed=None,
    unsafe=False,
    group=None,
    charset_list=False,
    quiet=False,
    benchmark=False,
):
    zora = Zora()
    zora.parser = argparse.ArgumentParser()

    zora.args = SimpleNamespace(
        length=length,
        seed=seed,
        unsafe=unsafe,
        group=group,
        charset_list=charset_list,
        quiet=quiet,
        benchmark=benchmark,
    )

    return zora


def test_length_is_required():
    zora = make_zora(length=None)

    with pytest.raises(SystemExit):
        zora.validate_args()


def test_length_not_required_for_charset_list():
    zora = make_zora(
        length=None,
        charset_list=True,
    )

    with pytest.raises(SystemExit) as exc_info:
        zora.validate_args()

    assert exc_info.value.code == 0


def test_seed_requires_unsafe():
    zora = make_zora(
        seed="test-seed",
        unsafe=False,
    )

    with pytest.raises(SystemExit):
        zora.validate_args()


def test_seed_allowed_with_unsafe():
    zora = make_zora(
        seed="test-seed",
        unsafe=True,
    )

    zora.validate_args()


def test_no_seed_without_unsafe_is_valid():
    zora = make_zora(
        seed=None,
        unsafe=False,
    )

    zora.validate_args()


def test_group_cannot_be_greater_than_length():
    zora = make_zora(
        length=8,
        group=9,
    )

    with pytest.raises(SystemExit):
        zora.validate_args()


def test_group_equal_to_length_is_valid():
    zora = make_zora(
        length=8,
        group=8,
    )

    zora.validate_args()


def test_group_smaller_than_length_is_valid():
    zora = make_zora(
        length=16,
        group=4,
    )

    zora.validate_args()


def test_no_group_is_valid():
    zora = make_zora(
        length=16,
        group=None,
    )

    zora.validate_args()


def test_charset_list_exits_successfully():
    zora = make_zora(
        length=None,
        charset_list=True,
    )

    with pytest.raises(SystemExit) as exc_info:
        zora.validate_args()

    assert exc_info.value.code == 0


def test_charset_list_does_not_require_length():
    zora = make_zora(
        length=None,
        charset_list=True,
    )

    with pytest.raises(SystemExit) as exc_info:
        zora.validate_args()

    assert exc_info.value.code == 0


def test_unsafe_mode_is_valid():
    zora = make_zora(
        unsafe=True,
    )

    zora.validate_args()


def test_unsafe_quiet_mode_is_valid():
    zora = make_zora(
        unsafe=True,
        quiet=True,
    )

    zora.validate_args()


def test_unsafe_benchmark_mode_is_valid():
    zora = make_zora(
        unsafe=True,
        benchmark=True,
    )

    zora.validate_args()


def test_benchmark_mode_is_valid():
    zora = make_zora(
        benchmark=True,
    )

    zora.validate_args()


def test_quiet_mode_is_valid():
    zora = make_zora(
        quiet=True,
    )

    zora.validate_args()


def test_normal_arguments_are_valid():
    zora = make_zora(
        length=32,
        seed=None,
        unsafe=False,
        group=4,
        quiet=False,
        benchmark=False,
    )

    zora.validate_args()


def test_seed_with_unsafe_and_benchmark_is_valid():
    zora = make_zora(
        length=32,
        seed="benchmark-seed",
        unsafe=True,
        benchmark=True,
    )

    zora.validate_args()