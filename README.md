# RingSort

> A fast and cross-platform Python CLI tool for automatically organizing files into categorized folders.


\

RingSort helps you clean messy directories by automatically sorting files into organized folders based on their extensions.

## Example

Turn this:

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
├── Images/
│   └── photo.jpg
├── Documents/
│   └── report.pdf
├── Videos/
│   └── movie.mp4
└── Music/
    └── music.mp3
```

---

## Features

* 📁 Automatic file organization
* 🖼 Categorization of Images, Videos, Music, Documents, Archives, Code, Executables, and Others
* 👀 Dry-run mode to preview changes before execution
* 🔄 Recursive directory scanning
* 🔍 Hash-based duplicate detection
* 🔒 Safe filename conflict handling without silent overwrites
* 📝 Optional verbose logging and log file output
* ⚡ Fast and lightweight CLI experience
* 💻 Cross-platform support:

  * Windows
  * Linux
  * macOS

---

## Installation

### From PyPI

```bash
pip install ringsort
```

Upgrade:

```bash
pip install --upgrade ringsort
```

### From Source

```bash
git clone https://github.com/ammagicring/ringsort.git

cd ringsort

python -m venv .venv
```

Activate environment:

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install:

```bash
pip install -U pip
pip install -e .
```

---

## Quick Start

Organize a directory:

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

---

## Usage

Basic:

```bash
ringsort PATH
```

Dry run:

```bash
ringsort PATH --dry-run
```

Recursive sorting:

```bash
ringsort PATH --recursive
```

Verbose mode:

```bash
ringsort PATH --verbose
```

Save logs:

```bash
ringsort PATH --log-file ringsort.log
```

Help:

```bash
ringsort --help
```

---

## Dry Run

Preview planned operations without modifying files:

```bash
ringsort ~/Downloads --dry-run
```

Example:

```text
[DRY RUN]

movie.mp4 -> Videos/
image.png -> Images/
document.pdf -> Documents/

✓ 3 files scanned
✓ Dry run complete (no files moved)
```

---

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

---

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run quality checks:

```bash
ruff check src tests
```

```bash
mypy
```

```bash
pytest
```

---

## Roadmap

* [x] v1.0.0 Initial release
* [ ] v1.1 Configurable category mappings
* [ ] v1.2 Undo support via transaction log
* [ ] v1.3 Watch mode for automatic sorting
* [ ] v2.0 Plugin-based rules engine

---

## Contributing

Contributions are welcome!

Please read `CONTRIBUTING.md` before opening a pull request.

---

## License

This project is licensed under the MIT License.

See LICENSE.

---

## Author

Created by **Amir Mohammad Mohammadi**

GitHub:
https://github.com/ammagicring
