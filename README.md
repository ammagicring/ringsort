# RingSort

`RingSort` is a cross-platform Python CLI that organizes files inside a directory by moving them into folders based on file extensions.

## Features (v1.0)

- Organize files by extension into categories (Images, Videos, Music, Documents, Archives, Code, Executables, Others)
- Ignore directories (only files are moved)
- Automatically create destination folders
- Safe handling of duplicate filenames
- Graceful handling of permission errors (continues organizing)
- Cross-platform: Windows, Linux, macOS

## Installation

### From source (recommended)

```bash
git clone https://github.com/ammagicring/ringsort
cd RingSort
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -U pip
pip install -e .
```

### Install test dependencies

```bash
pip install -e ".[dev]"
```

## Usage

The installed command is `organizer`.

### Organize a directory

```bash
organizer organize ~/Downloads
```

Example output:

```
✓ 15 files scanned
✓ 4 Images
✓ 2 Documents
✓ 3 Videos
✓ Done in 0.42 seconds
```

### Dry run (no moves)

```bash
organizer organize ~/Downloads --dry-run
```

## Project Structure

```
RingSort/
├── src/
│   └── organizer/
│       ├── __init__.py
│       ├── main.py
│       ├── scanner.py
│       ├── mover.py
│       ├── categories.py
│       ├── logger.py
│       └── utils.py
├── tests/
├── README.md
├── LICENSE
├── pyproject.toml
├── .gitignore
└── requirements.txt
```

## Development

Run tests:

```bash
pytest
```

## Roadmap

- v1.1: optional recursive mode
- v1.2: configurable category mappings via config file
- v1.3: `--undo` support (transaction log)
- v2.0: plug-in categories and rules engine

## License

MIT. See `LICENSE`.
