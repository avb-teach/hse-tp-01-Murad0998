#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Нужно 2 аргумента" >&2
    echo "Использовались: $0 <input_dir> <output_dir>" >&2
    exit 1
fi

input_dir="$1"
output_dir="$2"

if [ ! -d "$input_dir" ]; then
    echo "Нет директории" >&2
    exit 2
fi

mkdir -p "$output_dir" || {
    echo "Ошибка вывода" >&2
    exit 3
}

python3 collect_files.py "$input_dir" "$output_dir"