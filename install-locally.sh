#!/usr/bin/bash

rm -Rf dist
uv build --wheel
uv tool install --reinstall ./dist/*.whl --force
echo "Installed module"

