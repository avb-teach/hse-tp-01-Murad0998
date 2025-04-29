#!/usr/bin/env python3
import os
import sys
import shutil
import argparse

def create_unique_filename(folder: str, original: str) -> str:
    main_part, suffix = os.path.splitext(original)
    num = 1
    while True:
        if (num > 1):
            result_name = f"{main_part}__{num}{suffix}"
        else:
            result_name = original
        check_path = os.path.join(folder, result_name)
        if not os.path.isfile(check_path):
            return result_name
        num += 1

def process_hierarchy(source: str, dest: str, limit: int | None):
    for cur_dir, _, items in os.walk(source):
        relative = os.path.relpath(cur_dir, source)
        if relative == '.':
            level=0
        else:
            level=relative.count(os.path.sep)+1
        if limit is not None and level > limit:
            continue
        path_segments = []
        if (relative != '.'):
            path_segments = relative.split(os.path.sep)
            if (limit):
                path_segments = path_segments[:limit]
        
        new_location = os.path.join(dest, *path_segments)
        os.makedirs(new_location, exist_ok=True)
        for item in items:
            origin = os.path.join(cur_dir, item)
            unique_name = create_unique_filename(new_location, item)
            destination = os.path.join(new_location, unique_name)
            shutil.copy2(origin, destination)

def main():
    cli_parser = argparse.ArgumentParser()
    cli_parser.add_argument('src')
    cli_parser.add_argument('dst')
    cli_parser.add_argument('--max_depth', type=int, default=None)
    params = cli_parser.parse_args()
    if not os.path.isdir(params.src):
        sys.exit(1)
    try:
        os.makedirs(params.dst, exist_ok=True)
        process_hierarchy(params.src, params.dst, params.max_depth)
    except OSError:
        sys.exit(2)

if __name__ == '__main__':
    main()