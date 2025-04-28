#!/usr/bin/env python3
import os
import sys
import shutil
import argparse

def get_unique_filename(dst_dir, base_name):
    name, ext = os.path.splitext(base_name)
    counter = 1
    new_name = base_name
    while os.path.exists(os.path.join(dst_dir, new_name)):
        new_name = f"{name}_{counter}{ext}"
        counter += 1
    return new_name

def process_directory(src_dir, dst_dir, max_depth=None):
    src_dir = os.path.normpath(src_dir)
    for dirpath, _, filenames in os.walk(src_dir):
        dirpath = os.path.normpath(dirpath)
        depth = dirpath[len(src_dir):].count(os.sep)
        if dirpath == src_dir:
            depth = 0
        if max_depth is not None and depth >= max_depth:
            continue
        for fname in filenames:
            src_path = os.path.join(dirpath, fname)
            if not os.path.isfile(src_path):
                continue
            new_name = get_unique_filename(dst_dir, fname)
            dest_path = os.path.join(dst_dir, new_name)
            shutil.copy2(src_path, dest_path)

def main():
    parser = argparse.ArgumentParser(description="Сбор файлов в плоскую структуру")
    parser.add_argument("input_dir", help="Исходная директория")
    parser.add_argument("output_dir", help="Целевая директория")
    parser.add_argument("--max_depth", type=int, help="Максимальная глубина обхода", default=None)
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.input_dir):
        print(f"Ошибка: {args.input_dir} не является директорией", file=sys.stderr)
        sys.exit(2)
    
    os.makedirs(args.output_dir, exist_ok=True)
    process_directory(args.input_dir, args.output_dir, args.max_depth)

if __name__ == "__main__":
    main()