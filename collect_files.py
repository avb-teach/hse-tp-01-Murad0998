#!/usr/bin/env python3
import os
import sys
import shutil
import argparse

def get_unique_filename(dst_dir: str, base_name: str) -> str:
    """Генерирует уникальное имя файла с суффиксом _N"""
    name, ext = os.path.splitext(base_name)
    counter = 1
    while True:
        new_name = f"{name}_{counter}{ext}" if counter > 1 else base_name
        full_path = os.path.join(dst_dir, new_name)
        if not os.path.exists(full_path):
            return new_name
        counter += 1

def process_directory(src_dir: str, dst_dir: str, max_depth: int|None = None):
    src_dir = os.path.normpath(src_dir)
    for root, _, files in os.walk(src_dir):
        rel = os.path.relpath(root, src_dir)
        parts = [] if rel == '.' else rel.split(os.sep)
        depth = len(parts)

        if max_depth is None:
            target_subdirs = []
        else:
            if depth <= max_depth:
                target_subdirs = parts
            else:
                target_subdirs = parts[:max_depth]

        dst_path_dir = os.path.join(dst_dir, *target_subdirs)
        os.makedirs(dst_path_dir, exist_ok=True)

        for fname in files:
            new_fname = get_unique_filename(dst_path_dir, fname)
            shutil.copy2(os.path.join(root, fname),
                         os.path.join(dst_path_dir, new_fname))


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Копирует файлы из директории с сохранением структуры до указанной глубины')
    parser.add_argument('input_dir')
    parser.add_argument('output_dir')
    parser.add_argument('--max_depth', type=int, default=None)
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.input_dir):
        print(f"Ошибка: {args.input_dir} не существует", file=sys.stderr)
        sys.exit(1)
        
    os.makedirs(args.output_dir, exist_ok=True)
    process_directory(args.input_dir, args.output_dir, args.max_depth)

if __name__ == '__main__':
    main()