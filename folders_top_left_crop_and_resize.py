import os
import subprocess
import sys

def process_subfolders(base_folder, target_folder, target_size):
    """Enumerates subfolders in the base folder and processes each using the top_left_crop_and_resize.py script."""
    if not os.path.isdir(base_folder):
        print("The specified base directory does not exist.")
        return

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    for root, dirs, _ in os.walk(base_folder):
        for dir_name in dirs:
            source_subfolder = os.path.join(root, dir_name)
            relative_subfolder = os.path.relpath(source_subfolder, base_folder)
            target_subfolder = os.path.join(target_folder, relative_subfolder)

            # Print the operation
            print(f"Processing {source_subfolder} to {target_subfolder}")

            # Call the top_left_crop_and_resize.py script
            subprocess.run([
                sys.executable, 'top_left_crop_and_resize.py',
                source_subfolder,
                target_subfolder,
                str(target_size)
            ])

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python process_subfolders.py <base_folder> <target_folder> <target_size>")
        sys.exit(1)

    BASE_FOLDER = sys.argv[1]
    TARGET_FOLDER = sys.argv[2]
    TARGET_SIZE = int(sys.argv[3])

    process_subfolders(BASE_FOLDER, TARGET_FOLDER, TARGET_SIZE)
