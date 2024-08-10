import os
import shutil
import sys

def move_files_to_base(base_folder):
    """Move all files from subfolders to the base folder and delete the subfolders."""
    if not os.path.isdir(base_folder):
        print("The specified base directory does not exist.")
        return

    for root, dirs, files in os.walk(base_folder, topdown=False):
        for file_name in files:
            source_file = os.path.join(root, file_name)
            destination_file = os.path.join(base_folder, file_name)

            try:
                # Move file to base folder
                print(f"Moving {source_file} to {destination_file}")
                shutil.move(source_file, destination_file)
            except Exception as e:
                print(f"Error moving file {source_file}: {e}")

        # Remove empty directories
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                if not os.listdir(dir_path):  # Check if the directory is empty
                    print(f"Removing empty directory {dir_path}")
                    os.rmdir(dir_path)
            except Exception as e:
                print(f"Error removing directory {dir_path}: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python move_files_to_base.py <base_folder>")
        sys.exit(1)

    BASE_FOLDER = sys.argv[1]
    move_files_to_base(BASE_FOLDER)
