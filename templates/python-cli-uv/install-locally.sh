#!/usr/bin/bash

rm -Rf dist
uv build --wheel
uv tool install ./dist/*.whl
echo "Installed module"

