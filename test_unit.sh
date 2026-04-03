# add -k to filter per filename
uv run python -m unittest discover -s ./tests/unit -v "$@"
