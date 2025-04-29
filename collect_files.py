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

def process_directory(src_dir: str, dst_dir: str, max_depth: int | None = None) -> None:
    src_dir = os.path.normpath(src_dir)
    for root, _, files in os.walk(src_dir):
        rel_path = os.path.relpath(root, src_dir)
        current_depth = rel_path.count(os.sep) + 1 if rel_path != '.' else 0
        
        if max_depth is not None and current_depth > max_depth:
            continue

        if max_depth is not None:
            parts = rel_path.split(os.sep)[:max_depth]
            target_dir = os.path.join(dst_dir, *parts)
        else:
            target_dir = dst_dir
            
        os.makedirs(target_dir, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            dst_name = get_unique_filename(target_dir, file)
            dst_file = os.path.join(target_dir, dst_name)
            shutil.copy2(src_file, dst_file)

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