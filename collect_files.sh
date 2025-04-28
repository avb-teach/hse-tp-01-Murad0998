#!/bin/bash

# Проверяем, что Python 3 доступен
if ! command -v python3 &> /dev/null; then
    echo "Ошибка: Python 3 не установлен"
    exit 1
fi

# Вызываем Python-скрипт с переданными аргументами
python3 collect_files.py "$@"