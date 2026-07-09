# RingSort Documentation

## Overview

RingSort organizes files in a target directory by extension. Category folders are created automatically inside the target directory.

## Categories

| Category | Examples |
| -------- | -------- |
| Images | `.jpg`, `.png`, `.webp` |
| Videos | `.mp4`, `.mkv`, `.mov` |
| Music | `.mp3`, `.wav`, `.flac` |
| Documents | `.pdf`, `.docx`, `.txt` |
| Archives | `.zip`, `.rar`, `.7z` |
| Code | `.py`, `.js`, `.ts`, `.json` |
| Executables | `.exe`, `.msi`, `.deb` |
| Others | Unrecognized extensions |

## Duplicate Handling

RingSort uses SHA-256 content hashes to detect duplicates:

- **Exact duplicate**: skipped, source file remains in place
- **Name conflict, different content**: safely renamed (for example, `report (1).pdf`)
- **No silent overwrites**

## Recursive Mode

With `--recursive`, RingSort scans subdirectories but skips files already inside category folders to avoid re-processing organized content.

## Logging

- Default level: `INFO`
- `--verbose`: enables `DEBUG`
- `--log-file`: writes logs to a file in addition to the console

## Exit Codes

| Code | Meaning |
| ---- | ------- |
| `0` | Success |
| `1` | One or more files failed to move |
| `2` | Invalid path or CLI usage error |
