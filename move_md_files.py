import os
import shutil
import argparse

def move_specific_files(src_dir, dest_dir):
    # Create the destination directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Define the file extensions to move
    file_extensions_to_move = [".md", ".png", ".svg", ".puml"]

    # Walk through the source directory recursively
    for root, dirs, files in os.walk(src_dir):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for file in files:
            if any(file.endswith(ext) for ext in file_extensions_to_move):
                # Get the full file path
                src_file_path = os.path.join(root, file)
                
                # Preserve the directory structure (optional)
                rel_path = os.path.relpath(root, src_dir)
                dest_subdir = os.path.join(dest_dir, rel_path)
                
                # Avoid moving files into themselves
                if os.path.commonpath([src_file_path, dest_dir]) == dest_dir:
                    continue

                # Create the destination subdirectory if it doesn't exist
                if not os.path.exists(dest_subdir):
                    os.makedirs(dest_subdir)
                
                # Construct the destination file path
                if file == "README.md":
                    dest_file_path = os.path.join(dest_subdir, "index.md")
                else:
                    dest_file_path = os.path.join(dest_subdir, file)

                # Move the file
                shutil.move(src_file_path, dest_file_path)
                print(f"Moved: {src_file_path} -> {dest_file_path}")

if __name__ == "__main__":
    # Parse arguments from the command line
    parser = argparse.ArgumentParser(description="Move specific file types recursively to a new folder.")
    parser.add_argument("src_dir", type=str, help="The source directory to search for files")
    parser.add_argument("dest_dir", type=str, nargs='?', default="docs", help="The destination directory where files will be moved (default: 'docs')")
    
    args = parser.parse_args()

    # Only run if src_dir is set
    if args.src_dir:
        # Move the files
        move_specific_files(args.src_dir, args.dest_dir)