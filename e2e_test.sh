# add -k to filter by test name
# add -p to filter by file name
# ./e2e_test.sh -p "test_fais.py"
uv run python -m unittest discover -s tests/e2e -v "$@"
