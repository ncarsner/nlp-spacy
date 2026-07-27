# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/). This project has not
adopted semantic version tags, so entries are grouped by date instead.

## [2026-07-27]
### Added
- `.docx` and `.pdf` file input support to the `types` CLI tool (`read_text_from_file()`), via
  `python-docx` and `pypdf` (PR #4, superseding earlier drafts #2/#3)
- Real-file integration tests for both `.docx` and `.pdf` reading, alongside mocked unit tests
- `README.md` and this changelog
### Changed
- Optional-format imports (`docx`, `pypdf`) made lazy, scoped to their own branches, so the base
  CLI no longer requires them for plain-text input
- `pypdf.PdfReader` now opened via a context manager for deterministic file-handle cleanup
- `uv.lock` regenerated for the new `python-docx` dependency
### Fixed
- N/A
### Removed
- Stray root-level `main.py` scratch file

## [2026-03-13]
### Added
- `simplify` and `types` CLI tools (`utils/simplify.py`, `utils/sentence_types.py`) — text
  simplification and sentence-type classification, registered as console scripts
### Fixed
- Package discovery, build-backend syntax, and Python version constraints in `pyproject.toml`

## [2026-01-11]
### Added
- `run_coverage.py` coverage runner script
### Changed
- Expanded test coverage across `functions.py`, `sample_counter.py`, `zipfs.py`

## [2026-01-09]
### Added
- Test suite: `test_component_counter.py`, `test_functions.py`, `test_pdf_reader.py`,
  `test_sample_counter.py`, `test_zipfs.py`
- `__init__.py` files for the `tests/` and `utils/` packages
### Removed
- `requirements.txt`, in favor of `uv`/`pyproject.toml` dependency management

## [2026-01-08]
### Added
- `ROADMAP.md` outlining planned development
- Migrated to a `uv`-managed project (`pyproject.toml`, `uv.lock`)
- `main.py` entry point

## [2025-06-21] – [2025-06-23]
### Added
- `utils/component_counter.py` — counts grammatical components in text
- `chatbot_basic.py` — a simple rule-based chatbot over packaged fundamentals data
  (`data/packaged/fundamentals.json`)
### Changed
- Docstring updates and additional test phrases in `component_counter.py`
### Fixed
- Minor correction in `zipfs.py`

## [2025-02-27]
### Added
- `.vscode/settings.json`
### Fixed
- Minor fixes in `pdf_reader.py`

## [2024-11-07]
### Added
- Initial project scaffold
- Zipf's Law word-frequency utilities (`utils/functions.py`, `utils/zipfs.py`) over sample
  historical speech texts (`data/raw/*.txt`)
- PDF word-frequency utilities (`utils/pdf_reader.py`, `utils/sample_counter.py`), with a sample
  PDF fixture (`data/raw/mlb_rules_2023.pdf`)
- MIT License
