#!/bin/bash

if ! command -v python3 &> /dev/null; then
    echo "Ошибка: Python 3 не установлен"
    exit 1
fi

python3 collect_files.py "$@"