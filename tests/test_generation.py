from types import SimpleNamespace
from zora.cli import Zora


def make_zora(
    length=16,
    count=1,
    charset="abc123",
    unsafe=False,
    seed=None,
    prefix="",
    suffix="",
    group=None,
    sep="-",
):
    zora = Zora()

    zora.args = SimpleNamespace(
        length=length,
        count=count,
        unsafe=unsafe,
        seed=seed,
        prefix=prefix,
        suffix=suffix,
        group=group,
        sep=sep,
    )

    zora.charset = charset

    return zora


def test_generate_one_key():
    zora = make_zora(length=16)

    zora.generate_keys()

    assert len(zora.lines) == 1
    assert len(zora.lines[0]) == 16


def test_generate_multiple_keys():
    zora = make_zora(length=16, count=10)

    zora.generate_keys()

    assert len(zora.lines) == 10


def test_generated_key_uses_only_charset():
    charset = "abc123"
    zora = make_zora(length=100, charset=charset)

    zora.generate_keys()

    key = zora.lines[0]

    assert all(char in charset for char in key)


def test_generated_keys_have_correct_length():
    zora = make_zora(length=32, count=10)

    zora.generate_keys()

    assert all(len(key) == 32 for key in zora.lines)


def test_generate_different_keys():
    zora = make_zora(length=32, count=10)

    zora.generate_keys()

    assert len(set(zora.lines)) > 1


def test_prefix_is_added():
    zora = make_zora(
        length=16,
        prefix="zora-",
    )

    zora.generate_keys()

    assert zora.lines[0].startswith("zora-")
    assert len(zora.lines[0]) == 21


def test_suffix_is_added():
    zora = make_zora(
        length=16,
        suffix="-key",
    )

    zora.generate_keys()

    assert zora.lines[0].endswith("-key")
    assert len(zora.lines[0]) == 20


def test_prefix_and_suffix_are_added():
    zora = make_zora(
        length=16,
        prefix="zora-",
        suffix="-key",
    )

    zora.generate_keys()

    assert zora.lines[0].startswith("zora-")
    assert zora.lines[0].endswith("-key")
    assert len(zora.lines[0]) == 25


def test_grouping():
    zora = make_zora(
        length=16,
        group=4,
        sep="-",
    )

    zora.generate_keys()

    key = zora.lines[0]

    parts = key.split("-")

    assert len(parts) == 4
    assert all(len(part) == 4 for part in parts)


def test_custom_group_separator():
    zora = make_zora(
        length=16,
        group=4,
        sep=":",
    )

    zora.generate_keys()

    key = zora.lines[0]

    assert key.count(":") == 3


def test_grouping_preserves_key_characters():
    charset = "abc123"

    zora = make_zora(
        length=16,
        charset=charset,
        group=4,
        sep="-",
    )

    zora.generate_keys()

    key_without_separators = zora.lines[0].replace("-", "")

    assert len(key_without_separators) == 16
    assert all(char in charset for char in key_without_separators)


def test_seeded_unsafe_generation_is_reproducible():
    zora1 = make_zora(
        length=32,
        count=5,
        unsafe=True,
        seed="test-seed",
    )

    zora2 = make_zora(
        length=32,
        count=5,
        unsafe=True,
        seed="test-seed",
    )

    zora1.generate_keys()
    zora2.generate_keys()

    assert zora1.lines == zora2.lines


def test_different_seeds_produce_different_keys():
    zora1 = make_zora(
        length=32,
        unsafe=True,
        seed="seed-one",
    )

    zora2 = make_zora(
        length=32,
        unsafe=True,
        seed="seed-two",
    )

    zora1.generate_keys()
    zora2.generate_keys()

    assert zora1.lines != zora2.lines


def test_seed_does_not_affect_csprng_generation():
    zora1 = make_zora(
        length=32,
        unsafe=False,
        seed="same-seed",
    )

    zora2 = make_zora(
        length=32,
        unsafe=False,
        seed="same-seed",
    )

    zora1.generate_keys()
    zora2.generate_keys()

    # secrets.choice() is not controlled by random.seed().
    # It should not be expected to produce identical results.
    assert len(zora1.lines) == 1
    assert len(zora2.lines) == 1


def test_lines_are_appended():
    zora = make_zora(length=16, count=3)

    zora.lines.append("existing")

    zora.generate_keys()

    assert len(zora.lines) == 4
    assert zora.lines[0] == "existing"