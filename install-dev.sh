#!/usr/bin/env bash
uv sync
uv tool install --editable --force .

echo "Installed fais as an editable uv tool."
echo "Code changes in this repository will be reflected automatically."
echo "If 'fais' is not on your PATH yet, run: uv tool update-shell"
