#!/usr/bin/env python3
import os
import sys
import shutil
import argparse

def find_existing_files(output_folder: str):
    existing = {}
    for fname in os.listdir(output_folder):
        if os.path.isfile(os.path.join(output_folder, fname)):
            base = fname.rsplit('.', 1)
            name = base[0] if len(base) > 1 else fname
            ext = f'.{base[1]}' if len(base) > 1 else ''
            parts = name.rsplit('_', 1)
            if len(parts) > 1 and parts[1].isdigit():
                num = int(parts[1])
                existing[f'{parts[0]}{ext}'] = max(existing.get(f'{parts[0]}{ext}', 0), num)
            else:
                existing[fname] = 1
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
            counter = 1
            while True:
                dest_path = os.path.join(dst_dir, new_name)
                if not os.path.exists(dest_path):
                    break
                if base_name in file_counter:
                    counter = file_counter[base_name] + 1
                else:
                    counter = 1
                new_name = f"{name_parts[0]}_{counter}{name_parts[1]}"
                file_counter[base_name] = counter
            try:
                shutil.copy2(src_path, dest_path)
                file_counter[base_name] = counter
                print(f"Скопирован: {src_path} -> {dest_path}")
            except Exception as e:
                print(f"Ошибка при копировании {src_path}: {e}", file=sys.stderr)
                sys.exit(1)

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