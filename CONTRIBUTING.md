# Contributing to RingSort

Thank you for your interest in contributing to RingSort!

## Getting Started

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-change`
3. Install development dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Development Workflow

Run the full quality suite before opening a pull request:

```bash
ruff check src tests
mypy
pytest
```

## Pull Request Guidelines

- Keep changes focused and well-scoped
- Add or update tests for behavior changes
- Update documentation when user-facing behavior changes
- Follow existing code style and naming conventions
- Write clear commit messages

## Code Style

- Use `pathlib` instead of `os.path` where possible
- Add type hints to public functions
- Add docstrings to public functions
- Prefer small, focused functions over large modules

## Reporting Issues

Please include:

- Operating system and Python version
- Exact command used
- Expected behavior
- Actual behavior
- Minimal reproduction steps when possible

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
