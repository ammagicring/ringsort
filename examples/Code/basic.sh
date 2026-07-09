#!/usr/bin/env bash
# Basic RingSort examples

# Organize Downloads
ringsort ~/Downloads

# Preview changes without moving files
ringsort ~/Downloads --dry-run

# Include nested files
ringsort ~/Desktop --recursive

# Verbose logging
ringsort ~/Downloads --verbose

# Save logs to a file
ringsort ~/Downloads --log-file ./ringsort.log
