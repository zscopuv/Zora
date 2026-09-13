from types import SimpleNamespace

from zora.cli import Zora


def make_zora(
    prefix="",
    suffix="",
    group=None,
    sep="-",
):
    zora = Zora()
    zora.args = SimpleNamespace(
        prefix=prefix,
        suffix=suffix,
        group=group,
        sep=sep,
    )
    return zora


def test_format_key_without_formatting():
    zora = make_zora()

    assert zora.format_key("abcdefghijkl") == "abcdefghijkl"


def test_format_key_with_prefix():
    zora = make_zora(prefix="zora-")

    assert zora.format_key("abcdefghijkl") == "zora-abcdefghijkl"


def test_format_key_with_suffix():
    zora = make_zora(suffix="-key")

    assert zora.format_key("abcdefghijkl") == "abcdefghijkl-key"


def test_format_key_with_prefix_and_suffix():
    zora = make_zora(
        prefix="zora-",
        suffix="-key",
    )

    assert zora.format_key("abcdefghijkl") == "zora-abcdefghijkl-key"


def test_format_key_with_grouping():
    zora = make_zora(group=4)

    assert zora.format_key("abcdefghijkl") == "abcd-efgh-ijkl"


def test_format_key_with_custom_separator():
    zora = make_zora(
        group=4,
        sep=":",
    )

    assert zora.format_key("abcdefghijkl") == "abcd:efgh:ijkl"


def test_format_key_with_multi_character_separator():
    zora = make_zora(
        group=4,
        sep="---",
    )

    assert zora.format_key("abcdefghijkl") == "abcd---efgh---ijkl"


def test_format_key_with_prefix_suffix_and_grouping():
    zora = make_zora(
        prefix="zora-",
        suffix="-key",
        group=4,
        sep="-",
    )

    assert zora.format_key("abcdefghijkl") == "zora-abcd-efgh-ijkl-key"


def test_format_key_with_group_larger_than_key():
    zora = make_zora(group=20)

    assert zora.format_key("abcdefghijkl") == "abcdefghijkl"


def test_format_key_with_group_equal_to_key_length():
    zora = make_zora(group=12)

    assert zora.format_key("abcdefghijkl") == "abcdefghijkl"


def test_format_key_with_group_not_divisible_by_key_length():
    zora = make_zora(group=5)

    assert zora.format_key("abcdefghijkl") == "abcde-fghij-kl"


def test_format_key_preserves_original_characters():
    zora = make_zora(
        group=3,
        sep=":",
    )

    result = zora.format_key("a1B!xY9@")

    assert result.replace(":", "") == "a1B!xY9@"


def test_format_key_with_empty_prefix_and_suffix():
    zora = make_zora(
        prefix="",
        suffix="",
        group=4,
    )

    assert zora.format_key("12345678") == "1234-5678"