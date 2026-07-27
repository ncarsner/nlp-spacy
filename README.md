# nlp-spacy

Natural Language Processing tools built on spaCy and NLTK.

## CLI tools

Installed as console scripts (`simplify`, `types`) via `pyproject.toml`.

### `types` — sentence type classifier

Classifies each sentence in a text as declarative, interrogative, imperative, or exclamatory.

```bash
types "Hello! How are you? Please sit down. I am fine."
types --file speech.txt --stats
types --file document.docx
types --file document.pdf --stats --output results.txt
```

Accepts `.txt`, `.docx`, and `.pdf` input files (`--file`/`-f`), or raw text as a positional
argument or `--text`/`-t`. Note: for `.docx` files, only body paragraph text is read — text
inside tables is not extracted.

### `simplify` — text simplifier

Simplifies complex text (legal, academic, technical) while preserving overall structure —
replacing jargon and verbose phrasing, simplifying passive voice, with adjustable aggressiveness.

```bash
simplify "Pursuant to the aforementioned agreement..."
simplify --file contract.txt --output simplified.txt --stats
simplify -f document.txt -o simple.txt --level aggressive
simplify --text "In the event that..." --diff
```

`--level` accepts `light`, `moderate` (default), or `aggressive`. `--diff` shows a before/after
comparison; `--stats` shows simplification statistics.

Both tools accept `--model` to select a different spaCy model (default: `en_core_web_sm`).

## Other utilities (`utils/`)

- `functions.py` / `zipfs.py` — Zipf's Law word-frequency analysis over sample speech texts
  (`data/raw/*.txt`)
- `pdf_reader.py` / `sample_counter.py` — word-frequency counting from PDF documents
- `component_counter.py` — counts grammatical components in text
- `chatbot_basic.py` — a simple rule-based chatbot over packaged fundamentals data

## Setup

Managed with [`uv`](https://docs.astral.sh/uv/):

```bash
uv sync
uv run types "Sample text"
```

## Project history

See [CHANGELOG.md](CHANGELOG.md) for what's changed, and [ROADMAP.md](ROADMAP.md) for planned
work.
