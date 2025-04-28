#!/usr/bin/env bash

if ! command -v python3 &> /dev/null; then
    echo "Ошибка: Python 3 не установлен" >&2
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/collect_files.py"

python3 "$PYTHON_SCRIPT" "$@"