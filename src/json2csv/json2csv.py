"""Convierte JSON (lista de objetos) a CSV. Funciona como filtro stdin/stdout."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from contextlib import ExitStack
from typing import Any, TextIO, cast


class ConversionError(Exception):
    """Error controlado durante la conversión."""


def _is_record(obj: object) -> bool:
    """Indica si ``obj`` es un objeto JSON (dict)."""
    return isinstance(obj, dict)


def flatten(obj: dict[str, Any], prefix: str = "") -> dict[str, Any]:
    """Aplana un dict anidado usando 'a.b' como nombre de columna."""
    out: dict[str, Any] = {}
    for key, value in obj.items():
        name = f"{prefix}{key}"
        if isinstance(value, dict):
            out.update(flatten(value, f"{name}."))
        elif isinstance(value, list):
            out[name] = json.dumps(value, ensure_ascii=False)
        else:
            out[name] = value
    return out


def convert(src: TextIO, dst: TextIO, delimiter: str = ",") -> int:
    """Lee JSON de ``src`` y escribe CSV en ``dst``. Devuelve filas escritas."""
    if len(delimiter) != 1:
        raise ConversionError("El delimitador debe ser un único carácter.")
    try:
        data: Any = json.load(src)
    except json.JSONDecodeError as exc:
        raise ConversionError(f"JSON inválido: {exc}") from exc
    items: Any = [data] if isinstance(data, dict) else data
    if not isinstance(items, list) or not all(_is_record(r) for r in items):
        raise ConversionError("Se esperaba un objeto o una lista de objetos.")
    records = cast("list[dict[str, Any]]", items)
    rows = [flatten(r) for r in records]
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    writer = csv.DictWriter(dst, fieldnames=columns, delimiter=delimiter)
    writer.writeheader()
    writer.writerows(rows)
    return len(rows)


def build_parser() -> argparse.ArgumentParser:
    """Arma el parser de argumentos."""
    parser = argparse.ArgumentParser(description="Convierte JSON a CSV.")
    parser.add_argument("-i", dest="input", help="archivo de entrada (default: stdin)")
    parser.add_argument("-o", dest="output", help="archivo de salida (default: stdout)")
    parser.add_argument(
        "-d", dest="delimiter", default=",", help="delimitador (default: ,)"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Punto de entrada. Devuelve código de salida."""
    args = build_parser().parse_args(argv)
    try:
        with ExitStack() as stack:
            src: TextIO = (
                stack.enter_context(open(args.input, encoding="utf-8"))
                if args.input
                else sys.stdin
            )
            dst: TextIO = (
                stack.enter_context(
                    open(args.output, "w", encoding="utf-8", newline="")
                )
                if args.output
                else sys.stdout
            )
            convert(src, dst, args.delimiter)
    except (ConversionError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
