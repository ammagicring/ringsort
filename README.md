# RingSort

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://github.com/ammagicring/ringsort/actions/workflows/tests.yml/badge.svg)](https://github.com/ammagicring/ringsort/actions/workflows/tests.yml)
[![Coverage](https://img.shields.io/badge/coverage-%E2%89%A580%25-brightgreen.svg)](https://github.com/ammagicring/ringsort)

RingSort is a cross-platform Python CLI that organizes files inside a directory by moving them into folders based on file extensions.

Turn a messy folder like this:

```text
Downloads/
├── photo.jpg
├── report.pdf
├── movie.mp4
└── music.mp3
```

Into this:

```text
Downloads/
├── Images/photo.jpg
├── Documents/report.pdf
├── Videos/movie.mp4
└── Music/music.mp3
```

## Features

- Simple CLI: `ringsort ~/Downloads`
- Extension-based categorization into Images, Videos, Music, Documents, Archives, Code, Executables, and Others
- Dry run preview with `--dry-run`
- Recursive sorting with `--recursive`
- Hash-based duplicate detection
- Safe renaming for filename conflicts (never silently overwrites files)
- Graceful handling of permission errors
- Optional verbose logging and log file output
- Cross-platform support for Windows, Linux, and macOS

## Installation

### From PyPI

```bash
pip install ringsort
```

### From source

```bash
git clone https://github.com/ammagicring/ringsort
cd ringsort
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -U pip
pip install -e .
```

### Development setup

```bash
pip install -e ".[dev]"
```

## Quick Start

```bash
ringsort ~/Downloads
```

Example output:

```text
✓ 15 files scanned
✓ 4 Images
✓ 2 Documents
✓ 3 Videos
✓ Done in 0.42 seconds
```

## Usage

```bash
ringsort PATH
ringsort PATH --dry-run
ringsort PATH --recursive
ringsort PATH --verbose
ringsort PATH --log-file ringsort.log
ringsort --help
```

### Dry run

Preview planned operations without changing the filesystem:

```bash
ringsort ~/Downloads --dry-run
```

Example output:

```text
[DRY RUN]
movie.mp4 -> Videos/
image.png -> Images/
document.pdf -> Documents/

✓ 3 files scanned
✓ 1 Videos
✓ 1 Images
✓ 1 Documents
✓ Dry run complete (no files moved)
✓ Done in 0.05 seconds
```

## Project Structure

```text
ringsort/
├── src/
│   └── ringsort/
│       ├── __init__.py
│       ├── cli.py
│       ├── scanner.py
│       ├── mover.py
│       ├── duplicates.py
│       ├── config.py
│       ├── logger.py
│       └── categories.py
├── tests/
├── docs/
├── examples/
├── .github/workflows/
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── LICENSE
├── pyproject.toml
└── requirements.txt
```

## Development

Run the quality checks locally:

```bash
ruff check src tests
mypy
pytest
```

## Roadmap

- v1.1: configurable category mappings
- v1.2: undo support via transaction log
- v1.3: watch mode for automatic sorting
- v2.0: plugin-based rules engine

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## License

MIT. See [LICENSE](LICENSE).
