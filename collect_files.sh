#!/bin/bash

if [ $# -ne 2 ]; then
    exit 1
fi

input_dir="$1"
output_dir="$2"

[ -d "$input_dir" ] || exit 2
mkdir -p "$output_dir" || exit 3

exec python3 ./collect_files.py "$input_dir" "$output_dir"