#!/usr/bin/env python3
import os
import sys
import shutil
import argparse

def find_existing_files(output_folder: str):
    existing = {}
    for fname in os.listdir(output_folder):
        if os.path.isfile(os.path.join(output_folder, fname)):
            base, ext = os.path.splitext(fname)
            parts = base.rsplit('_', 1)
            if len(parts) > 1 and parts[1].isdigit():
                num = int(parts[1])
                original_name = f"{parts[0]}{ext}"
                existing[original_name] = max(existing.get(original_name, 0), num)
            else:
                existing[fname] = 0
    return existing

def process_directory(src_dir: str, dst_dir: str, max_depth: int = None):
    file_counter = find_existing_files(dst_dir)
    
    for dirpath, _, filenames in os.walk(src_dir):
        depth = dirpath[len(src_dir):].count(os.sep)
        if max_depth is not None and depth >= max_depth:
            continue
        
        for fname in filenames:
            src_path = os.path.join(dirpath, fname)
            if not os.path.isfile(src_path):
                continue
            base_name = os.path.basename(src_path)
            name_parts = os.path.splitext(base_name)
            new_name = base_name
            counter = file_counter.get(base_name, 0) + 1
            while os.path.exists(os.path.join(dst_dir, new_name)):
                new_name = f"{name_parts[0]}_{counter}{name_parts[1]}"
                counter += 1
            shutil.copy2(src_path, os.path.join(dst_dir, new_name))
            file_counter[base_name] = counter - 1

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