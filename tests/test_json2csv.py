"""Tests de json2csv."""

import io
import json
from pathlib import Path

import pytest

from json2csv.json2csv import ConversionError, convert, main


def run(text: str, delim: str = ",") -> str:
    """Ejecuta convert sobre un texto."""
    out = io.StringIO()
    convert(io.StringIO(text), out, delim)
    return out.getvalue()


def test_basic() -> None:
    """Lista simple."""
    assert run('[{"a":1,"b":2}]').splitlines() == ["a,b", "1,2"]


def test_single_object_and_delimiter() -> None:
    """Objeto suelto y delimitador."""
    assert run('{"a":1,"b":2}', ";").splitlines() == ["a;b", "1;2"]


def test_nested_and_list() -> None:
    """Aplanado y listas."""
    out = run('[{"a":{"b":1},"c":[1,2]}]')
    assert out.splitlines()[0] == "a.b,c"


def test_missing_keys() -> None:
    """Claves distintas entre filas."""
    assert run('[{"a":1},{"b":2}]').splitlines()[0] == "a,b"


def test_invalid_json() -> None:
    """JSON roto."""
    with pytest.raises(ConversionError):
        run("{no")


def test_bad_structure() -> None:
    """Estructura inválida."""
    with pytest.raises(ConversionError):
        run("[1,2]")


def test_bad_delimiter() -> None:
    """Delimitador inválido."""
    with pytest.raises(ConversionError):
        run("[]", "ab")


def test_main_files(tmp_path: Path) -> None:
    """Modo archivo -i/-o."""
    i, o = tmp_path / "i.json", tmp_path / "o.csv"
    i.write_text(json.dumps([{"x": 1}]), encoding="utf-8")
    assert main(["-i", str(i), "-o", str(o)]) == 0
    assert o.read_text(encoding="utf-8").splitlines() == ["x", "1"]


def test_main_missing_file(tmp_path: Path) -> None:
    """Archivo inexistente."""
    assert main(["-i", str(tmp_path / "no.json")]) == 1


def test_main_stdio(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Modo filtro."""
    monkeypatch.setattr("sys.stdin", io.StringIO('[{"a":1}]'))
    assert main([]) == 0
    assert capsys.readouterr().out.splitlines() == ["a", "1"]
