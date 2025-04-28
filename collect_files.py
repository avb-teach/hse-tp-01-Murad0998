import os
import shutil
import sys

def copy_files(src, dst):
    try:
        for root, _, files in os.walk(src):
            for filename in files:
                src_path = os.path.join(root, filename)
                dst_path = os.path.join(dst, filename)
                
                if os.path.exists(dst_path):
                    base, ext = os.path.splitext(filename)
                    counter = 1
                    while True:
                        new_name = f"{base}_{counter}{ext}"
                        new_dst = os.path.join(dst, new_name)
                        if not os.path.exists(new_dst):
                            shutil.copy2(src_path, new_dst)
                            break
                        counter += 1
                else:
                    shutil.copy2(src_path, dst_path)
    except Exception as e:
        print(f"Critical error: {str(e)}", file=sys.stderr)
        sys.exit(4)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Invalid arguments count", file=sys.stderr)
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    
    if not os.path.isdir(input_dir):
        print("Input directory is invalid", file=sys.stderr)
        sys.exit(2)
    
    os.makedirs(output_dir, exist_ok=True)
    copy_files(input_dir, output_dir)
    sys.exit(0)