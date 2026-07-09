# Security Policy

## Supported Versions

| Version | Supported |
| ------- | --------- |
| 1.0.x   | Yes       |

## Reporting a Vulnerability

If you discover a security vulnerability in RingSort, please report it responsibly.

1. Do not open a public GitHub issue for security-sensitive reports
2. Contact the maintainers through a private channel if available
3. Include:
   - A clear description of the issue
   - Steps to reproduce
   - Potential impact
   - Suggested remediation if you have one

We aim to acknowledge reports within 7 days and provide a remediation plan when
possible.

## Scope

RingSort is a local file-management CLI. Security concerns may include:

- Unsafe file operations
- Path traversal or unintended file overwrites
- Permission escalation through mishandled symlinks
- Information disclosure through logging

We take reports in these areas seriously and will prioritize fixes accordingly.
