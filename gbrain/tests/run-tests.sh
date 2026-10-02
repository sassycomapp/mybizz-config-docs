#!/usr/bin/env bash
# Runs the mb-doc-check tests against the installed script.  Usage: bash run-tests.sh
set -euo pipefail
D="$(mktemp -d)"
cp "$(dirname "$0")"/test_*.py "$D"/
cp /mnt/c/mybizz/scripts/mb-doc-check.py "$D"/
cd "$D" && python3 -W ignore -m unittest discover -p 'test_*.py' 2>&1 | tail -4
