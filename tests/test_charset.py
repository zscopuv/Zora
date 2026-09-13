import argparse
from types import SimpleNamespace

import pytest

from zora.cli import Zora


def make_zora(charset):
    zora = Zora()
    zora.parser = argparse.ArgumentParser()
    zora.args = SimpleNamespace(charset=charset)
    return zora


def test_build_digits_preset():
    zora = make_zora("@digits")

    zora.build_charset()

    assert zora.charset == "0123456789"


def test_build_letters_preset():
    zora = make_zora("@letters")

    zora.build_charset()

    assert zora.charset == (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    )


def test_build_lower_preset():
    zora = make_zora("@lower")

    zora.build_charset()

    assert zora.charset == "abcdefghijklmnopqrstuvwxyz"


def test_build_upper_preset():
    zora = make_zora("@upper")

    zora.build_charset()

    assert zora.charset == "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def test_build_combined_presets():
    zora = make_zora("@letters@digits")

    zora.build_charset()

    assert zora.charset == (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"
    )


def test_build_multiple_presets():
    zora = make_zora("@lower@upper@digits")

    zora.build_charset()

    assert len(zora.charset) == 62
    assert all(char in zora.charset for char in "abcdefghijklmnopqrstuvwxyz")
    assert all(char in zora.charset for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    assert all(char in zora.charset for char in "0123456789")


def test_build_literal_characters():
    zora = make_zora("abc123")

    zora.build_charset()

    assert zora.charset == "abc123"


def test_build_mixed_preset_and_literals():
    zora = make_zora("@digitsXYZ")

    zora.build_charset()

    assert zora.charset == "0123456789XYZ"


def test_build_preset_and_literals_with_duplicates():
    zora = make_zora("@digits123")

    zora.build_charset()

    assert zora.charset == "0123456789"


def test_build_removes_duplicate_characters():
    zora = make_zora("aaabbbccc")

    zora.build_charset()

    assert zora.charset == "abc"


def test_build_preserves_character_order():
    zora = make_zora("zxyabc")

    zora.build_charset()

    assert zora.charset == "zxyabc"


def test_build_removes_duplicates_while_preserving_order():
    zora = make_zora("aabbccab")

    zora.build_charset()

    assert zora.charset == "abc"


def test_build_hex_preset():
    zora = make_zora("@hex")

    zora.build_charset()

    assert zora.charset == "0123456789ABCDEF"


def test_build_base62_preset():
    zora = make_zora("@base62")

    zora.build_charset()

    assert len(zora.charset) == 62


def test_build_url_preset():
    zora = make_zora("@url")

    zora.build_charset()

    assert len(zora.charset) > 0


def test_build_multiple_same_presets():
    zora = make_zora("@digits@digits")

    zora.build_charset()

    assert zora.charset == "0123456789"


def test_unknown_preset_raises_system_exit():
    zora = make_zora("@doesnotexist")

    with pytest.raises(SystemExit):
        zora.build_charset()


def test_empty_charset_fails_validation():
    zora = make_zora("")

    zora.build_charset()

    with pytest.raises(SystemExit):
        zora.validate_charset()


def test_single_character_charset_fails_validation():
    zora = make_zora("a")

    zora.build_charset()

    with pytest.raises(SystemExit):
        zora.validate_charset()


def test_duplicate_characters_resulting_in_one_character_fails_validation():
    zora = make_zora("aaaa")

    zora.build_charset()

    assert zora.charset == "a"

    with pytest.raises(SystemExit):
        zora.validate_charset()


def test_two_character_charset_passes_validation():
    zora = make_zora("ab")

    zora.build_charset()
    zora.validate_charset()

    assert zora.charset == "ab"


def test_large_charset_passes_validation():
    zora = make_zora("@letters@digits")

    zora.build_charset()
    zora.validate_charset()

    assert len(zora.charset) == 62


def test_special_characters():
    zora = make_zora("!#$%")

    zora.build_charset()

    assert zora.charset == "!#$%"