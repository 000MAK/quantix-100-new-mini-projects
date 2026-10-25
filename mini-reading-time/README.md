# Reading Time Calculator

Estimate reading duration from word count and reading speed.

## Requirements

- Python 3.10 or newer
- Python standard library only; no runtime packages to install

## Run

From this folder:

```bash
python main.py sample_input.json
```

Or pipe JSON to standard input:

```bash
python main.py < sample_input.json
```

## Input contract

Send one JSON object. See [`sample_input.json`](sample_input.json) for the expected fields and [`sample_output.json`](sample_output.json) for an example result.

## Tests

```bash
python -m unittest -v
```

## Safety notes

This project runs locally and makes no network requests. It does not execute submitted code or send data to a service. Treat files and output as untrusted until you review them. This is a small educational utility, not a security certification or financial advice.
