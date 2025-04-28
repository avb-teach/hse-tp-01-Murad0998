#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Error: Exactly two arguments required" >&2
    echo "Usage: $0 <input_dir> <output_dir>" >&2
    exit 1
fi

input_dir="$1"
output_dir="$2"

if [ ! -d "$input_dir" ]; then
    echo "Error: Input directory does not exist" >&2
    exit 2
fi

mkdir -p "$output_dir" || {
    echo "Error: Failed to create output directory" >&2
    exit 3
}

python3 collect_files.py "$input_dir" "$output_dir"