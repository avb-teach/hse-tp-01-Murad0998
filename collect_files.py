#!/usr/bin/env python3
import os
import sys
import shutil
import argparse

def generate_unique_name(dst_dir: str, filename: str) -> str:
    base_name, ext = os.path.splitext(filename)
    counter = 1
    while True:
        new_name = f"{base_name}_{counter}{ext}" if counter > 1 else filename
        full_path = os.path.join(dst_dir, new_name)
        if not os.path.exists(full_path):
            return new_name
        counter += 1

def copy_files(src_root: str, dst_root: str, max_depth: int | None):
    for root, _, files in os.walk(src_root):
        rel_path = os.path.relpath(root, src_root)
        if rel_path != '.':
            current_depth = rel_path.count(os.sep) + 1
        else:
            current_depth = 0
        if max_depth is not None and current_depth > max_depth:
            continue

        if max_depth is not None:
            path_parts = rel_path.split(os.sep)[:max_depth]
        else:
            if rel_path != '.':
                path_parts = rel_path.split(os.sep)
            else:
                path_parts = []
        
        target_dir = os.path.join(dst_root, *path_parts)
        os.makedirs(target_dir, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(target_dir, generate_unique_name(target_dir, file))
            shutil.copy2(src_file, dst_file)

def main():
    parser = argparse.ArgumentParser(description='Копирование файлов с сохранением структуры до указанной глубины')
    parser.add_argument('input_dir', help='Исходная директория')
    parser.add_argument('output_dir', help='Целевая директория')
    parser.add_argument('--max_depth', type=int, help='Максимальная глубина вложенности', default=None)
    
    args = parser.parse_args()
    if not os.path.isdir(args.input_dir):
        sys.exit(1)
    os.makedirs(args.output_dir, exist_ok=True)
    copy_files(args.input_dir, args.output_dir, args.max_depth)

if __name__ == '__main__':
    main()