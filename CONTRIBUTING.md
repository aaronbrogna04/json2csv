# Cómo contribuir

## Paso 1: preparar el entorno

Clonar el repositorio y crear un entorno virtual:

```sh
git clone https://github.com/aaronbrogna04/json2csv.git
cd json2csv
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Paso 2: hacer los cambios

Crear una rama, hacer los cambios y agregar los tests correspondientes:

```sh
git checkout -b nombre-de-la-rama
```

## Paso 3: verificar los controles

Antes de abrir un pull request, verificar que pasen todos los controles de calidad:

```sh
ruff check . && black --check . && pydocstyle --convention=pep257 src tests
mypy && pyright && bandit -r src && pytest
```

## Paso 4: documentar el cambio

Registrar el cambio en `CHANGELOG.md` y actualizar `VERSION` si corresponde.
