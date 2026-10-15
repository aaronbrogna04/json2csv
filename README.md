# json2csv

Herramienta de línea de comandos en Python que convierte archivos JSON (un objeto o una lista de objetos) a CSV. Funciona como **filtro**: lee de un archivo o de la entrada estándar y escribe en un archivo o en la salida estándar.

## Uso

    python -m json2csv [-i input.json] [-o output.csv] [-d delimitador]

- Sin `-i`, lee de la entrada estándar.
- Sin `-o`, escribe en la salida estándar.
- Sin `-d`, usa la coma como delimitador.
- Los objetos anidados se aplanan como columnas `a.b` y las listas se serializan como JSON.
- Ante errores (archivo inexistente, JSON inválido, delimitador inválido) informa `Error: ...` por la salida de error y termina con código 1.

Ejemplos:

    echo '[{"a":1,"b":{"c":2}}]' | python -m json2csv
    python -m json2csv -i datos.json -o salida.csv -d ";"

## Desarrollo

    python3 -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    pip install -e .

Controles de calidad (los mismos que ejecuta la integración continua):

    ruff check .
    black --check .
    pydocstyle --convention=pep257 src tests
    mypy
    pyright
    bandit -r src
    pytest            # cobertura mínima exigida: 85 %
    pdoc -o docs/api json2csv

## Información del proyecto

- Versión: archivo `VERSION`. Build: archivo `BUILD`.
- Cambios: `CHANGELOG.md`. Prompts de IA utilizados: `CONTEXT.md`.
- Licencia: MIT (`LICENSE`).
