# fais

`fais` is a command-line LLM-based AI agent for day-to-day operations.

## Local install

For the project virtual environment:

```sh
uv sync
```

This is enough for `uv run fais ...`, but it does not make a globally available `fais` command auto-update from your working tree.

For a globally available `fais` CLI that tracks local code changes:

```sh
./install-dev.sh
```

If `fais` is still not found after installation, [add uv's tool executables to your shell](https://docs.astral.sh/uv/concepts/tools/#tool-executables):

```sh
uv tool update-shell
```

## Built version

```
./build.sh
```

## Usage

```sh
fais "prompt" ./file1 ./file2
```

## Technologies

- LangChain for the agent loop
- uv for setup
- Good old code, limited use of AI except for debugging annoying errors

## References and docs

- https://setuptools.pypa.io/
- https://docs.langchain.com/
- https://docs.astral.sh/


## About

"Fais" is French for "do" and pronounces  pronounces "[fɛ]", like "fay" without the "y" part. Do not pronounce the "s" or the French will mock you for some reason, and it will be conflated with "FAISS" library of algorithms. [You can listen to the proper pronounciation here](https://www.youtube.com/watch?v=y_RkLxMarTw).
