#!/usr/bin/env python3
import os
import sys
import shutil
import argparse

def get_unique_filename(dst_dir: str, base_name: str) -> str:
    name, ext = os.path.splitext(base_name)
    counter = 1
    new_name = base_name
    while os.path.exists(os.path.join(dst_dir, new_name)):
        new_name = f"{name}{counter}{ext}"
        counter += 1
    return new_name


def process_directory(src_dir: str, dst_dir: str, max_depth: int | None = None) -> None:
    src_dir = os.path.normpath(src_dir)
    for root, dirs, files in os.walk(src_dir):
        rel_path = os.path.relpath(root, src_dir)
        if rel_path == '.':
            parts = []
            depth = 0
        else:
            parts = rel_path.split(os.sep)
            depth = len(parts)
        if max_depth is not None and depth > max_depth:
            continue

        if max_depth is None:
            target_dir = dst_dir
        else:
            target_dir = os.path.join(dst_dir, *parts)
        os.makedirs(target_dir, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            dst_name = get_unique_filename(target_dir, file)
            dst_file = os.path.join(target_dir, dst_name)
            shutil.copy2(src_file, dst_file)


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Собрать файлы из директории в плоскую структуру или с ограниченной глубиной')
    parser.add_argument('input_dir', help='Путь к исходной директории')
    parser.add_argument('output_dir', help='Путь к целевой директории')
    parser.add_argument(
        '--max_depth', type=int, default=None,
        help='Максимальная глубина обхода (необязательно)'
    )

    args = parser.parse_args()

    if not os.path.isdir(args.input_dir):
        print(f"Ошибка: {args.input_dir} не является директорией", file=sys.stderr)
        sys.exit(2)
    os.makedirs(args.output_dir, exist_ok=True)

    process_directory(args.input_dir, args.output_dir, args.max_depth)

if __name__ == '__main__':
    main()
