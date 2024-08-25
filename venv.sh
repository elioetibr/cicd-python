#!/usr/bin/env bash

VERSION="$(sed -E 's|python.*"~(.*)"|\1|g' < pyproject.toml)"

python"${VERSION}" -m venv ".venv"
source ".venv/bin/activate"
which python
python -V

cat <<-TOML > poetry.toml
[virtualenvs]
create = true
in-project = true
prefer-active-python = true
TOML

python3 -m pip install --upgrade pip

poetry env info
poetry env info --version
poetry env info --path
poetry env info --executable
poetry lock
poetry install --sync
