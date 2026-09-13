import argparse
import json
import re
import xml.etree.ElementTree as ET
from types import SimpleNamespace

import pytest

from zora.cli import Zora


ANSI_ESCAPE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def strip_ansi(text):
    return ANSI_ESCAPE.sub("", text)


def make_zora(
    lines,
    output_format="text",
    output=None,
    quiet=False,
):
    zora = Zora()
    zora.parser = argparse.ArgumentParser()

    zora.args = SimpleNamespace(
        format=output_format,
        output=output,
        quiet=quiet,
    )

    zora.lines = lines

    return zora


def test_text_output(capsys):
    zora = make_zora(["abc123", "XYZ789"])

    zora.output()

    captured = capsys.readouterr()
    output = strip_ansi(captured.out)

    assert "abc123" in output
    assert "XYZ789" in output
    assert output.endswith("\n")


def test_text_output_multiple_keys(capsys):
    zora = make_zora([
        "first",
        "second",
        "third",
    ])

    zora.output()

    captured = capsys.readouterr()
    output = strip_ansi(captured.out)

    assert output == "first\nsecond\nthird\n"


def test_json_output(capsys):
    zora = make_zora(
        ["abc123", "XYZ789"],
        output_format="json",
    )

    zora.output()

    captured = capsys.readouterr()
    output = strip_ansi(captured.out)
    data = json.loads(output)

    assert data == {
        "keys": [
            "abc123",
            "XYZ789",
        ]
    }


def test_json_output_contains_keys(capsys):
    zora = make_zora(
        ["one", "two"],
        output_format="json",
    )

    zora.output()

    captured = capsys.readouterr()
    output = strip_ansi(captured.out)

    assert '"keys"' in output
    assert '"one"' in output
    assert '"two"' in output


def test_csv_output(capsys):
    zora = make_zora(
        ["abc123", "XYZ789"],
        output_format="csv",
    )

    zora.output()

    captured = capsys.readouterr()
    output = strip_ansi(captured.out)

    lines = output.splitlines()

    assert lines[0] == "key"
    assert lines[1] == "abc123"
    assert lines[2] == "XYZ789"


def test_csv_output_header(capsys):
    zora = make_zora(
        ["test"],
        output_format="csv",
    )

    zora.output()

    captured = capsys.readouterr()
    output = strip_ansi(captured.out)

    assert output.startswith("key\r\n")


def test_xml_output(capsys):
    zora = make_zora(
        ["abc123", "XYZ789"],
        output_format="xml",
    )

    zora.output()

    captured = capsys.readouterr()
    output = strip_ansi(captured.out)

    root = ET.fromstring(output)

    assert root.tag == "zora"

    keys = root.find("keys")

    assert keys is not None
    assert [element.text for element in keys.findall("key")] == [
        "abc123",
        "XYZ789",
    ]


def test_xml_output_structure(capsys):
    zora = make_zora(
        ["test"],
        output_format="xml",
    )

    zora.output()

    captured = capsys.readouterr()
    output = strip_ansi(captured.out)

    root = ET.fromstring(output)

    assert root.tag == "zora"
    assert len(root.findall("./keys/key")) == 1
    assert root.find("./keys/key").text == "test"


def test_yaml_output(capsys):
    yaml = pytest.importorskip("yaml")

    zora = make_zora(
        ["abc123", "XYZ789"],
        output_format="yml",
    )

    zora.output()

    captured = capsys.readouterr()
    output = strip_ansi(captured.out)
    data = yaml.safe_load(output)

    assert data == {
        "keys": [
            "abc123",
            "XYZ789",
        ]
    }


def test_yaml_output_contains_keys(capsys):
    pytest.importorskip("yaml")

    zora = make_zora(
        ["one", "two"],
        output_format="yml",
    )

    zora.output()

    captured = capsys.readouterr()
    output = strip_ansi(captured.out)

    assert "keys:" in output
    assert "one" in output
    assert "two" in output


def test_output_to_file(tmp_path):
    output_file = tmp_path / "keys.txt"

    zora = make_zora(
        ["abc123", "XYZ789"],
        output_format="text",
        output=str(output_file),
    )

    zora.output()

    assert output_file.exists()
    assert output_file.read_text(encoding="utf-8") == (
        "abc123\n"
        "XYZ789\n"
    )


def test_json_output_to_file(tmp_path):
    output_file = tmp_path / "keys.json"

    zora = make_zora(
        ["abc123", "XYZ789"],
        output_format="json",
        output=str(output_file),
    )

    zora.output()

    data = json.loads(
        output_file.read_text(encoding="utf-8")
    )

    assert data == {
        "keys": [
            "abc123",
            "XYZ789",
        ]
    }


def test_csv_output_to_file(tmp_path):
    output_file = tmp_path / "keys.csv"

    zora = make_zora(
        ["abc123", "XYZ789"],
        output_format="csv",
        output=str(output_file),
    )

    zora.output()

    assert output_file.read_text(encoding="utf-8") == (
        "key\n"
        "abc123\n"
        "XYZ789\n"
    )


def test_xml_output_to_file(tmp_path):
    output_file = tmp_path / "keys.xml"

    zora = make_zora(
        ["abc123", "XYZ789"],
        output_format="xml",
        output=str(output_file),
    )

    zora.output()

    root = ET.parse(output_file).getroot()

    assert root.tag == "zora"
    assert [
        element.text
        for element in root.findall("./keys/key")
    ] == [
        "abc123",
        "XYZ789",
    ]


def test_yaml_output_to_file(tmp_path):
    yaml = pytest.importorskip("yaml")

    output_file = tmp_path / "keys.yml"

    zora = make_zora(
        ["abc123", "XYZ789"],
        output_format="yml",
        output=str(output_file),
    )

    zora.output()

    data = yaml.safe_load(
        output_file.read_text(encoding="utf-8")
    )

    assert data == {
        "keys": [
            "abc123",
            "XYZ789",
        ]
    }


def test_empty_lines_text_output(capsys):
    zora = make_zora([])

    zora.output()

    captured = capsys.readouterr()
    output = strip_ansi(captured.out)

    assert output == "\n"


def test_empty_lines_json_output(capsys):
    zora = make_zora(
        [],
        output_format="json",
    )

    zora.output()

    captured = capsys.readouterr()
    output = strip_ansi(captured.out)
    data = json.loads(output)

    assert data == {
        "keys": []
    }


def test_unsupported_output_format():
    zora = make_zora(
        ["test"],
        output_format="invalid",
    )

    with pytest.raises(SystemExit):
        zora.output()